# Camera Trap para Observação de Animais (Raspberry Pi Zero 2 W + HC-SR04 + Módulo de câmera OV5647)

Câmera que grava vídeos automaticamente quando um animal aparece na frente do sensor. Ela usa um Raspberry Pi Zero 2 W, um módulo de câmera OV5647 e um sensor ultrassônico HC-SR04.

## Sobre o projeto

*Projeto desenvolvido no curso de Ciência da Computação sob a tutela do [Prof. Herbert Rocha](https://github.com/hbgit), Universidade Federal de Roraima (UFRR), 2026.2.*

O objetivo é observar animais sem a presença humana. O sistema fica parado no local, detecta quando algo se aproxima e salva um vídeo que **inclui os segundos anteriores ao disparo**. Assim o vídeo mostra o animal chegando. Cada visita também fica registrada num arquivo CSV com data, hora e duração.

## Conteúdo do repositório

```
camera_trap/
├── src/cameratrap/        Código-fonte em Python
│   ├── config.py          Todos os valores ajustáveis (pinos, tempos, resolução)
│   ├── logica.py          Calibração, filtro de presença e máquina de estados (sem hardware)
│   ├── sensor.py          Leitura do HC-SR04
│   ├── camera.py          Buffer circular e gravação de vídeo
│   ├── armazenamento.py   Nomes de arquivo, log CSV, conversão para .mp4
│   ├── app.py             Laço principal que junta tudo
│   └── __main__.py        Permite rodar com `python3 -m cameratrap`
├── tests/                 Testes que rodam no computador, sem Raspberry Pi
├── scripts/               Utilitários (ex.: teste_sensor.py para testar as ligações)
├── systemd/               Serviço para iniciar o programa sozinho no boot
├── docs/                  Requisitos, ligações, manual de operação e guia do Doxygen
│   ├── reports/           Relatório técnico, comparação com a literatura, análise da FSM, montagem
│   └── img/               Diagramas (e fontes em img/fontes/) e fotos do projeto
├── assets/                Imagens usadas no README
├── Doxyfile               Configuração da documentação do código (Doxygen)
└── README.md
```

## Hardware

| Componente | Função |
|---|---|
| Raspberry Pi Zero 2 W | Controla tudo e grava os vídeos |
| Módulo de câmera OV5647 e cabo para Pi Zero | Captura do vídeo |
| Sensor ultrassônico HC-SR04 | Detecta quando algo se aproxima |
| Resistores de 1 kΩ e 2 kΩ | Divisor de tensão para o pino Echo (5 V → 3,3 V) |
| Cartão microSD (de preferência "High Endurance") | Sistema e vídeos |
| Fonte 5 V / powerbank | Alimentação |

## Software utilizado

- Raspberry Pi OS Lite (sem interface gráfica, acesso por SSH)
- Python 3, com as bibliotecas [gpiozero](https://gpiozero.readthedocs.io/) e [Picamera2](https://github.com/raspberrypi/picamera2)
- ffmpeg (conversão de `.h264` para `.mp4`)
- Doxygen e Graphviz (documentação do código)

## Como funciona

O programa é uma **máquina de estados** com dois estados:

1. **Calibração** (ao ligar): mede por 5 s a distância "normal" com a área vazia, por exemplo até uma parede ou o fundo de um comedouro.
2. **ESPERANDO:** a câmera fica ligada guardando os últimos 3 s de vídeo na memória. O sensor mede a distância 10 vezes por segundo. Se algo ficar 15 cm mais perto que o normal em **3 leituras seguidas**, o programa passa a gravar.
3. **GRAVANDO:** o vídeo é salvo no cartão, incluindo os 3 s guardados. A gravação termina quando o animal sai e fica 5 s fora, ou quando o vídeo chega a 60 s.
4. Ao terminar, a visita é registrada em `visitas.csv`. O vídeo é convertido para `.mp4`, e o programa volta a esperar, depois de uma pausa de 5 s.

Todos esses valores podem ser ajustados em [`src/cameratrap/config.py`](src/cameratrap/config.py).

## Pinagem (Raspberry Pi Zero 2 W)

| HC-SR04 | Pino físico | GPIO | Observação |
|---|---|---|---|
| VCC | 2 | 5 V | |
| GND | 6 | GND | |
| Trig | 16 | GPIO23 | Ligação direta |
| Echo | 18 | GPIO24 | **Pelo divisor de tensão:** 1 kΩ em série, 2 kΩ para o GND |

> ⚠️ **Nunca ligue o Echo direto no Raspberry Pi.** O sinal é de 5 V e pode queimar o GPIO. Detalhes em [docs/ligacoes.md](docs/ligacoes.md).

A câmera vai no conector CSI do Pi Zero.

## Relatório técnico

A documentação técnica completa está em [`docs/reports/`](docs/reports/):

- [Relatório técnico](docs/reports/relatorio_tecnico.md): arquitetura, inovação, testes, limitações e evolução
- [Comparação com a literatura](docs/reports/comparacao_literatura.md): quatro trabalhos acadêmicos sobre camera traps
- [Análise da máquina de estados](docs/reports/analise_maquina_estados.md): estados, transições e testes
- [Montagem física](docs/reports/montagem_fisica.md): posicionamento do sensor e lista de materiais

## Instalação e uso

Resumo; o passo a passo completo está no [manual de operação](docs/manual_de_operacao.md).

```bash
# No Raspberry Pi (pelo SSH)
sudo apt update
sudo apt install -y python3-picamera2 python3-gpiozero ffmpeg git

git clone <URL-DO-SEU-REPOSITORIO> camera_trap
cd camera_trap/src
python3 -m cameratrap        # deixe a frente do sensor vazia ao iniciar
```

Os vídeos e o arquivo `visitas.csv` ficam em `~/gravacoes`.

Para iniciar sozinho no boot, use o serviço em [`systemd/cameratrap.service`](systemd/cameratrap.service). As instruções estão no manual.

## Testes

A lógica de decisão (calibração, filtro e máquina de estados) não depende do hardware. Por isso ela pode ser testada **no computador**, sem Raspberry Pi. Na pasta raiz do projeto, rode:

```bash
python3 -m unittest -v
```

## Documentação do código (Doxygen)

O código é comentado no formato do Doxygen (`@brief`, `@param`, `@return`...). Para gerar a documentação em HTML, rode na pasta raiz do projeto:

```bash
doxygen Doxyfile
```

Depois abra `docs/doxygen/html/index.html` no navegador. Instalação e detalhes estão em [docs/doxygen.md](docs/doxygen.md).

## Autores

- Nome – [@ThiagoVieiraCamara](https://github.com/ThiagoVieiraCamara)

## Fotos

Fotos da montagem e dos registros ficam em [`docs/img/`](docs/img/).

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
