"""
@package cameratrap
@brief Camera trap com Raspberry Pi Zero W, módulo de câmera e sensor HC-SR04.

O pacote está dividido em módulos com uma responsabilidade cada:

| Módulo           | Responsabilidade                                         | Usa hardware? |
|------------------|----------------------------------------------------------|---------------|
| config           | Todos os valores ajustáveis do projeto                   | Não           |
| logica           | Calibração, filtro de presença e máquina de estados      | Não           |
| sensor           | Leitura do sensor ultrassônico HC-SR04                   | Sim (GPIO)    |
| camera           | Buffer circular e gravação de vídeo                      | Sim (câmera)  |
| armazenamento    | Nomes de arquivo, log CSV, conversão para .mp4           | Não           |
| app              | Junta tudo no laço principal                             | Sim           |

Os módulos sem hardware podem ser testados no computador (pasta `tests/`).
"""

## Versão do projeto.
__version__ = "1.0.0"
