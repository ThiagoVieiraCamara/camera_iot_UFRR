"""
@file camera.py
@brief Controle da câmera com buffer circular (Picamera2).

A câmera fica ligada o tempo todo, guardando os últimos segundos de
vídeo na memória. Quando a gravação começa, esses segundos vão para o
arquivo junto com o resto, então o vídeo mostra o animal chegando.
"""

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput


class Camera:
    """
    @brief Mantém o buffer circular e salva/para vídeos.
    """

    def __init__(self, resolucao, fps, bitrate, segundos_antes):
        """
        @param resolucao Tupla (largura, altura).
        @param fps Quadros por segundo.
        @param bitrate Taxa de bits do vídeo H.264.
        @param segundos_antes Segundos guardados de antes do disparo.
        """
        self._picam2 = Picamera2()
        config = self._picam2.create_video_configuration(
            main={"size": resolucao},
            controls={"FrameRate": fps},
        )
        self._picam2.configure(config)
        # repeat=True repete os cabeçalhos do H.264, para o vídeo poder
        # começar "no meio" da transmissão; iperiod=fps gera 1 quadro-chave por segundo.
        self._encoder = H264Encoder(bitrate=bitrate, repeat=True, iperiod=fps)
        self._encoder.output = CircularOutput(buffersize=fps * segundos_antes)

    def ligar(self):
        """@brief Liga a câmera e começa a encher o buffer."""
        self._picam2.start()
        self._picam2.start_encoder(self._encoder)

    def comecar_video(self, caminho):
        """
        @brief Começa a salvar o vídeo (incluindo o conteúdo do buffer).
        @param caminho Arquivo .h264 de destino.
        """
        self._encoder.output.fileoutput = str(caminho)
        self._encoder.output.start()

    def parar_video(self):
        """@brief Para de salvar o vídeo atual. O buffer continua ativo."""
        self._encoder.output.stop()

    def desligar(self):
        """@brief Desliga a câmera e libera o dispositivo."""
        self._picam2.stop_encoder()
        self._picam2.stop()
        self._picam2.close()
