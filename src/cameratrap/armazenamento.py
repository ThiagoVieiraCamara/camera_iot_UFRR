"""
@file armazenamento.py
@brief Arquivos: nomes dos vídeos, log CSV, espaço livre e conversão para .mp4.
"""

import csv
import logging
import shutil
import subprocess
import threading

log = logging.getLogger(__name__)

## Cabeçalho do arquivo CSV de visitas.
CABECALHO_CSV = ["inicio", "fim", "duracao_s", "distancia_min_cm", "arquivo"]


def tem_ffmpeg():
    """
    @brief Verifica se o ffmpeg está instalado.
    @return True se o comando `ffmpeg` existe.
    """
    return shutil.which("ffmpeg") is not None


def nome_do_video(pasta, quando):
    """
    @brief Monta o caminho do vídeo a partir da data e hora.
    @param pasta Pasta de destino (Path).
    @param quando Data e hora do início (datetime).
    @return Path no formato `AAAA-MM-DD_HH-MM-SS.h264`.
    """
    return pasta / (quando.strftime("%Y-%m-%d_%H-%M-%S") + ".h264")


def espaco_livre_mb(pasta):
    """
    @brief Espaço livre no cartão.
    @param pasta Qualquer pasta do cartão.
    @return Espaço livre em megabytes.
    """
    return shutil.disk_usage(pasta).free / 1_000_000


def registrar_visita(arquivo_log, inicio, fim, distancia_min, nome_arquivo):
    """
    @brief Acrescenta uma linha ao CSV de visitas (cria o arquivo se não existir).
    @param arquivo_log Caminho do CSV (Path).
    @param inicio Início da visita (datetime).
    @param fim Fim da visita (datetime).
    @param distancia_min Menor distância medida durante a visita, em metros.
    @param nome_arquivo Nome do arquivo de vídeo.
    """
    novo = not arquivo_log.exists()
    with arquivo_log.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(CABECALHO_CSV)
        w.writerow([
            inicio.isoformat(timespec="seconds"),
            fim.isoformat(timespec="seconds"),
            round((fim - inicio).total_seconds(), 1),
            round(distancia_min * 100, 1),
            nome_arquivo,
        ])


def converter_para_mp4(h264, fps):
    """
    @brief Converte .h264 em .mp4 sem recodificar (rápido).

    Se a conversão der certo, apaga o .h264. Se o ffmpeg não estiver
    instalado, não faz nada.

    @param h264 Caminho do arquivo .h264 (Path).
    @param fps Quadros por segundo do vídeo.
    @return True se converteu, False caso contrário.
    """
    if not tem_ffmpeg():
        return False
    mp4 = h264.with_suffix(".mp4")
    r = subprocess.run(
        ["nice", "-n", "10", "ffmpeg", "-y", "-loglevel", "error",
         "-framerate", str(fps), "-i", str(h264), "-c", "copy", str(mp4)],
        check=False,
    )
    if r.returncode == 0 and mp4.exists() and mp4.stat().st_size > 0:
        h264.unlink()
        return True
    mp4.unlink(missing_ok=True)  # não deixa um .mp4 quebrado para trás
    log.warning("Falha ao converter %s (o .h264 foi mantido)", h264.name)
    return False


def converter_em_segundo_plano(h264, fps):
    """
    @brief Roda converter_para_mp4 numa thread, sem travar o programa.
    @param h264 Caminho do arquivo .h264.
    @param fps Quadros por segundo do vídeo.
    """
    threading.Thread(target=converter_para_mp4, args=(h264, fps), daemon=True).start()


def converter_sobras(pasta, fps):
    """
    @brief Converte vídeos .h264 que ficaram para trás (ex.: Pi desligou no meio).
    @param pasta Pasta das gravações.
    @param fps Quadros por segundo dos vídeos.
    """
    for h264 in sorted(pasta.glob("*.h264")):
        converter_para_mp4(h264, fps)
