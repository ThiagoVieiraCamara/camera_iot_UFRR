"""
@file sensor.py
@brief Leitura do sensor ultrassônico HC-SR04.

Ligação (com divisor de tensão no Echo!):

| HC-SR04 | Raspberry Pi                                               |
|---------|------------------------------------------------------------|
| VCC     | Pino 2 (5 V)                                               |
| GND     | Pino 6 (GND)                                               |
| Trig    | Pino 16 (GPIO23)                                           |
| Echo    | 1 kΩ → pino 18 (GPIO24), com 2 kΩ do pino 18 para o GND    |
"""

import time

from gpiozero import DistanceSensor


class SensorUltrassonico:
    """
    @brief Encapsula o HC-SR04 usando a biblioteca gpiozero.

    Esta classe só mede distâncias. A decisão de "tem um animal ou não"
    fica em logica.FiltroPresenca.
    """

    def __init__(self, pino_trig, pino_echo, distancia_max, tamanho_media=5):
        """
        @param pino_trig GPIO ligado ao Trig.
        @param pino_echo GPIO ligado ao Echo (via divisor de tensão).
        @param distancia_max Distância máxima medida, em metros.
        @param tamanho_media Quantas medidas entram na média de cada leitura.
        """
        self._sensor = DistanceSensor(
            echo=pino_echo,
            trigger=pino_trig,
            max_distance=distancia_max,
            queue_len=tamanho_media,
        )

    def distancia(self):
        """
        @brief Distância atual até o objeto mais próximo.
        @return Distância em metros (no máximo, a distância máxima configurada).
        """
        return self._sensor.distance

    def coletar(self, segundos, intervalo):
        """
        @brief Faz várias leituras seguidas (usado na calibração).
        @param segundos Por quanto tempo medir.
        @param intervalo Tempo entre leituras, em segundos.
        @return Lista de distâncias, em metros.
        """
        time.sleep(1)  # deixa a fila de medidas da gpiozero encher
        leituras = []
        fim = time.monotonic() + segundos
        while time.monotonic() < fim:
            leituras.append(self.distancia())
            time.sleep(intervalo)
        return leituras

    def fechar(self):
        """@brief Libera os pinos GPIO."""
        self._sensor.close()
