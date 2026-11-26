"""
@file config.py
@brief Configurações do camera trap.

Todos os valores ajustáveis ficam aqui. Para mudar o comportamento do
projeto (distâncias, tempos, resolução...), edite só este arquivo.
"""

from pathlib import Path

# ============================== SENSOR ==============================

## GPIO ligado ao pino Trig do HC-SR04 (pino físico 16).
PINO_TRIG = 23

## GPIO ligado ao pino Echo do HC-SR04 (pino físico 18), passando pelo divisor de tensão.
PINO_ECHO = 24

## Distância máxima medida, em metros. Leituras acima disso viram esse valor.
DISTANCIA_MAX = 2.0

## Quantas medidas o sensor usa para fazer a média de cada leitura.
TAMANHO_MEDIA = 5

## Intervalo entre leituras, em segundos (0.1 = 10 leituras por segundo).
INTERVALO_LEITURA = 0.1

## Tempo, em segundos, medindo o fundo vazio na calibração.
TEMPO_CALIBRACAO = 5

## Quanto mais perto (em metros) que o fundo algo precisa ficar para disparar.
MARGEM = 0.15

## Leituras seguidas "perto" necessárias para considerar que há um animal.
LEITURAS_PARA_DISPARAR = 3

# ============================== CÂMERA ==============================

## Resolução do vídeo (largura, altura).
RESOLUCAO = (1280, 720)

## Quadros por segundo.
FPS = 25

## Taxa de bits do vídeo (qualidade x tamanho do arquivo).
BITRATE = 4_000_000

## Segundos de vídeo guardados de ANTES do disparo.
SEGUNDOS_ANTES = 3

# ============================ GRAVAÇÃO ==============================

## Continua gravando até X segundos depois que o animal sai.
SEGUNDOS_DEPOIS = 5

## Duração máxima de um único vídeo, em segundos.
DURACAO_MAXIMA = 60

## Pausa mínima entre um vídeo e o próximo, em segundos.
TEMPO_ESPERA = 5

## Não grava se o cartão tiver menos que isso livre (em MB).
ESPACO_MINIMO_MB = 500

## Quanto tempo esperar antes de tentar de novo quando o cartão está cheio (s).
ESPERA_CARTAO_CHEIO = 60

# ============================= ARQUIVOS =============================

## Pasta onde os vídeos e o log são salvos.
PASTA = Path.home() / "gravacoes"

## Arquivo CSV com o registro de cada visita.
ARQUIVO_LOG = PASTA / "visitas.csv"
