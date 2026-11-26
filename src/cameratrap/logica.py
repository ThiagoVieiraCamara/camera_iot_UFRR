"""
@file logica.py
@brief Lógica do camera trap, sem nenhum acesso a hardware.

Este módulo decide **quando** gravar. Ele não sabe nada de GPIO nem de
câmera: recebe números (distâncias e horários) e devolve decisões.
Por isso pode ser testado no computador, sem Raspberry Pi.
"""

import statistics
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Calibracao:
    """
    @brief Resultado da calibração do sensor.
    """

    ## Distância "normal" medida com a área vazia (mediana), em metros.
    fundo: float
    ## Abaixo desta distância (m) considera-se que há algo na frente.
    limite: float
    ## Diferença entre a maior e a menor leitura da calibração (m).
    variacao: float


def calcular_calibracao(leituras, margem):
    """
    @brief Calcula a distância de fundo e o limite de disparo.

    Usa a mediana das leituras, que ignora leituras malucas isoladas.

    @param leituras Lista de distâncias (m) medidas com a área vazia.
    @param margem Quanto mais perto que o fundo (m) algo precisa ficar para disparar.
    @return Um objeto Calibracao.
    @exception ValueError Se a lista de leituras estiver vazia.
    """
    if not leituras:
        raise ValueError("Nenhuma leitura para calibrar.")
    fundo = statistics.median(leituras)
    return Calibracao(
        fundo=fundo,
        limite=fundo - margem,
        variacao=max(leituras) - min(leituras),
    )


class FiltroPresenca:
    """
    @brief Decide se há algo na frente do sensor.

    Só considera presença depois de várias leituras seguidas abaixo do
    limite. Uma única leitura errada não dispara a gravação.
    """

    def __init__(self, limite, leituras_necessarias):
        """
        @param limite Distância (m) abaixo da qual a leitura conta como "perto".
        @param leituras_necessarias Leituras "perto" seguidas para confirmar presença.
        """
        ## Distância (m) abaixo da qual a leitura conta como "perto".
        self.limite = limite
        ## Leituras "perto" seguidas para confirmar presença.
        self.leituras_necessarias = leituras_necessarias
        self._seguidas = 0

    def atualizar(self, distancia):
        """
        @brief Processa uma nova leitura.
        @param distancia Distância medida, em metros.
        @return True se há presença confirmada, False caso contrário.
        """
        if distancia < self.limite:
            self._seguidas += 1
        else:
            self._seguidas = 0
        return self._seguidas >= self.leituras_necessarias

    def reiniciar(self):
        """@brief Zera a contagem de leituras seguidas."""
        self._seguidas = 0


class Estado(Enum):
    """@brief Estados da máquina de estados."""

    ## Câmera ligada, aguardando um animal.
    ESPERANDO = "esperando"
    ## Salvando vídeo no cartão.
    GRAVANDO = "gravando"


class Acao(Enum):
    """@brief O que o programa principal deve fazer após cada atualização."""

    ## Nada a fazer.
    NENHUMA = "nenhuma"
    ## Começar a salvar um vídeo.
    INICIAR_GRAVACAO = "iniciar"
    ## Parar o vídeo atual.
    PARAR_GRAVACAO = "parar"


class MaquinaEstados:
    """
    @brief Máquina de estados que decide quando começar e parar de gravar.

    @dot
    digraph estados {
        rankdir=LR;
        node [shape=box, style=rounded];
        ESPERANDO -> GRAVANDO [label="presença e fora da espera"];
        GRAVANDO -> GRAVANDO [label="presença"];
        GRAVANDO -> ESPERANDO [label="ausente por SEGUNDOS_DEPOIS\nou DURACAO_MAXIMA"];
    }
    @enddot

    Os horários são números em segundos (ex.: `time.monotonic()`), o que
    permite testar a máquina com horários inventados.
    """

    def __init__(self, segundos_depois, duracao_maxima, tempo_espera):
        """
        @param segundos_depois Segundos sem presença para encerrar o vídeo.
        @param duracao_maxima Duração máxima de um vídeo, em segundos.
        @param tempo_espera Pausa mínima entre um vídeo e o próximo, em segundos.
        """
        ## Segundos sem presença para encerrar o vídeo.
        self.segundos_depois = segundos_depois
        ## Duração máxima de um vídeo (s).
        self.duracao_maxima = duracao_maxima
        ## Pausa mínima entre vídeos (s).
        self.tempo_espera = tempo_espera
        ## Estado atual.
        self.estado = Estado.ESPERANDO
        self._inicio = 0.0
        self._ultimo_presente = 0.0
        self._proximo_permitido = float("-inf")

    @property
    def gravando(self):
        """@brief True se está no estado GRAVANDO."""
        return self.estado is Estado.GRAVANDO

    def atualizar(self, agora, presente):
        """
        @brief Avança a máquina de estados com uma nova leitura.
        @param agora Horário atual, em segundos.
        @param presente Se há presença confirmada (saída do FiltroPresenca).
        @return A Acao que o programa principal deve executar.
        """
        if self.estado is Estado.ESPERANDO:
            if presente and agora >= self._proximo_permitido:
                self.estado = Estado.GRAVANDO
                self._inicio = agora
                self._ultimo_presente = agora
                return Acao.INICIAR_GRAVACAO
            return Acao.NENHUMA

        # Estado GRAVANDO
        if presente:
            self._ultimo_presente = agora
        saiu = agora - self._ultimo_presente >= self.segundos_depois
        longo_demais = agora - self._inicio >= self.duracao_maxima
        if saiu or longo_demais:
            self.estado = Estado.ESPERANDO
            self._proximo_permitido = agora + self.tempo_espera
            return Acao.PARAR_GRAVACAO
        return Acao.NENHUMA

    def cancelar(self, agora, esperar):
        """
        @brief Cancela uma gravação que não pôde começar (ex.: cartão cheio).
        @param agora Horário atual, em segundos.
        @param esperar Segundos até poder tentar gravar de novo.
        """
        self.estado = Estado.ESPERANDO
        self._proximo_permitido = agora + esperar
