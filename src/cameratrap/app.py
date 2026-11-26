"""
@file app.py
@brief Programa principal: junta sensor, lógica, câmera e armazenamento.

Fluxo:
1. Calibra o sensor (mede o fundo vazio).
2. Liga a câmera com buffer circular.
3. A cada leitura, o FiltroPresenca diz se há um animal e a
   MaquinaEstados diz se deve começar ou parar um vídeo.
4. Cada visita é registrada no CSV e o vídeo é convertido para .mp4.
"""

import logging
import signal
import threading
import time
from datetime import datetime

from . import armazenamento as arm
from . import config
from .logica import Acao, FiltroPresenca, MaquinaEstados, calcular_calibracao

log = logging.getLogger("cameratrap")


def calibrar(sensor):
    """
    @brief Mede o fundo vazio e cria o filtro de presença.
    @param sensor Um sensor.SensorUltrassonico.
    @return Um logica.FiltroPresenca configurado.
    @exception SystemExit Se o fundo estiver perto demais para a margem.
    """
    log.info("Calibrando por %d s -- deixe a frente do sensor vazia...", config.TEMPO_CALIBRACAO)
    leituras = sensor.coletar(config.TEMPO_CALIBRACAO, config.INTERVALO_LEITURA)
    cal = calcular_calibracao(leituras, config.MARGEM)
    log.info(
        "Fundo: %.1f cm | dispara abaixo de %.1f cm | variação: %.1f cm",
        cal.fundo * 100, cal.limite * 100, cal.variacao * 100,
    )
    if cal.fundo >= config.DISTANCIA_MAX * 0.98:
        log.warning(
            "O sensor está lendo o máximo (%.0f cm). Ou não há nada atrás da área "
            "vigiada, ou o Echo não está chegando (confira os fios e o divisor).",
            config.DISTANCIA_MAX * 100,
        )
    if cal.variacao > config.MARGEM:
        log.warning("Leituras instáveis na calibração; pode haver disparos falsos.")
    if cal.limite <= 0.05:
        raise SystemExit("O fundo está perto demais do sensor para a MARGEM escolhida.")
    return FiltroPresenca(cal.limite, config.LEITURAS_PARA_DISPARAR)


def main():
    """@brief Inicia o camera trap e roda até receber Ctrl+C ou SIGTERM."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Importados aqui para que os outros módulos funcionem sem hardware.
    from .camera import Camera
    from .sensor import SensorUltrassonico

    config.PASTA.mkdir(parents=True, exist_ok=True)
    usar_mp4 = arm.tem_ffmpeg()
    if usar_mp4:
        threading.Thread(target=arm.converter_sobras,
                         args=(config.PASTA, config.FPS), daemon=True).start()
    else:
        log.warning("ffmpeg não encontrado: vídeos ficarão em .h264 "
                    "(instale com: sudo apt install ffmpeg)")

    # Ctrl+C ou "systemctl stop" encerram o programa de forma limpa.
    parar = threading.Event()
    signal.signal(signal.SIGINT, lambda *_: parar.set())
    signal.signal(signal.SIGTERM, lambda *_: parar.set())

    sensor = SensorUltrassonico(config.PINO_TRIG, config.PINO_ECHO,
                                config.DISTANCIA_MAX, config.TAMANHO_MEDIA)
    filtro = calibrar(sensor)
    maquina = MaquinaEstados(config.SEGUNDOS_DEPOIS, config.DURACAO_MAXIMA,
                             config.TEMPO_ESPERA)

    camera = Camera(config.RESOLUCAO, config.FPS, config.BITRATE, config.SEGUNDOS_ANTES)
    camera.ligar()
    time.sleep(2)  # a câmera ajusta a exposição e o buffer começa a encher
    log.info("Pronto! Vigiando...")

    arquivo = inicio = None
    dist_min = config.DISTANCIA_MAX

    def finalizar_video():
        camera.parar_video()
        fim = datetime.now()
        nome = arquivo.with_suffix(".mp4").name if usar_mp4 else arquivo.name
        arm.registrar_visita(config.ARQUIVO_LOG, inicio, fim, dist_min, nome)
        log.info("Vídeo salvo: %s (%.1f s)", nome, (fim - inicio).total_seconds())
        arm.converter_em_segundo_plano(arquivo, config.FPS)

    try:
        while not parar.is_set():
            agora = time.monotonic()
            d = sensor.distancia()
            acao = maquina.atualizar(agora, filtro.atualizar(d))

            if acao is Acao.INICIAR_GRAVACAO:
                if arm.espaco_livre_mb(config.PASTA) < config.ESPACO_MINIMO_MB:
                    log.warning("Cartão quase cheio! Não vou gravar.")
                    maquina.cancelar(agora, config.ESPERA_CARTAO_CHEIO)
                else:
                    inicio = datetime.now()
                    arquivo = arm.nome_do_video(config.PASTA, inicio)
                    dist_min = d
                    camera.comecar_video(arquivo)
                    log.info("Detectado a %.1f cm -- gravando %s", d * 100, arquivo.name)
            elif acao is Acao.PARAR_GRAVACAO:
                finalizar_video()

            if maquina.gravando:
                dist_min = min(dist_min, d)

            parar.wait(config.INTERVALO_LEITURA)
    finally:
        log.info("Encerrando...")
        if maquina.gravando:
            finalizar_video()
        camera.desligar()
        sensor.fechar()
