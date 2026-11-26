#!/usr/bin/env python3
"""
@file teste_sensor.py
@brief Mostra a distância lida pelo HC-SR04, para testar as ligações.

Uso (no Raspberry Pi, na pasta raiz do projeto):

    python3 scripts/teste_sensor.py

Passe a mão na frente do sensor: a distância deve mudar. Ctrl+C para sair.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cameratrap import config  # noqa: E402
from cameratrap.sensor import SensorUltrassonico  # noqa: E402


def main():
    """@brief Imprime a distância 5 vezes por segundo até Ctrl+C."""
    sensor = SensorUltrassonico(config.PINO_TRIG, config.PINO_ECHO,
                                config.DISTANCIA_MAX, config.TAMANHO_MEDIA)
    print("Lendo o sensor... (Ctrl+C para sair)")
    try:
        while True:
            print(f"{sensor.distancia() * 100:6.1f} cm")
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.fechar()


if __name__ == "__main__":
    main()
