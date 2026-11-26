# Manual de operação

## 1. Preparar o cartão SD (sem monitor)

1. Instale o **Raspberry Pi Imager** no computador ([raspberrypi.com/software](https://www.raspberrypi.com/software/)).
2. Escolha **Raspberry Pi Zero** e o sistema **Raspberry Pi OS Lite (32-bit)**, que fica em "Raspberry Pi OS (other)".
3. Na personalização, configure:
   - **Hostname:** ex.: `cameratrap`
   - **Usuário e senha:** só letras minúsculas e números, sem acentos
   - **Wi-Fi:** rede e senha, país **BR**. O Pi Zero W só conecta em redes **2,4 GHz**.
   - **SSH:** habilitado, com senha
4. Grave o cartão, coloque no Pi e ligue. O primeiro boot leva de **5 a 10 minutos**.

## 2. Acessar pelo computador (SSH)

```bash
ssh seuusuario@cameratrap.local
```

Use o **usuário do Raspberry Pi** que você criou no Imager, não o do seu computador. A senha não aparece enquanto você digita.

Se `cameratrap.local` não funcionar, use o IP do Pi, que aparece na página do roteador ou no app Fing.

## 3. Instalar o projeto

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-gpiozero ffmpeg git
git clone <URL-DO-SEU-REPOSITORIO> ~/camera_trap
```

Sem o Git, copie a pasta do computador para o Pi:

```bash
scp -r camera_trap seuusuario@cameratrap.local:~
```

## 4. Testar as peças separadamente

Câmera (grava 10 s):

```bash
rpicam-vid -n -t 10000 --width 1280 --height 720 -o teste.h264
```

Sensor:

```bash
cd ~/camera_trap
python3 scripts/teste_sensor.py
```

Passe a mão na frente do sensor: a distância deve mudar. Para sair, aperte `Ctrl+C`.

## 5. Rodar o programa

Deixe a frente do sensor **vazia**, porque ele calibra ao iniciar, e rode:

```bash
cd ~/camera_trap/src
python3 -m cameratrap
```

A saída esperada é parecida com esta:

```
Calibrando por 5 s -- deixe a frente do sensor vazia...
Fundo: 80.3 cm | dispara abaixo de 65.3 cm | variação: 1.2 cm
Pronto! Vigiando...
Detectado a 41.0 cm -- gravando 2026-11-26_14-02-11.h264
Vídeo salvo: 2026-11-26_14-02-11.mp4 (9.8 s)
```

Para parar, aperte `Ctrl+C`.

## 6. Iniciar sozinho no boot (serviço)

1. Abra `systemd/cameratrap.service` e troque `SEU_USUARIO` pelo seu usuário. Depois copie o arquivo:
   ```bash
   sudo cp ~/camera_trap/systemd/cameratrap.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now cameratrap
   ```
2. Comandos úteis:

| Para... | Comando |
|---|---|
| Ver as mensagens ao vivo | `journalctl -u cameratrap -f` |
| Parar | `sudo systemctl stop cameratrap` |
| Iniciar | `sudo systemctl start cameratrap` |
| Não iniciar mais no boot | `sudo systemctl disable cameratrap` |

**Só um programa usa a câmera por vez.** Pare o serviço antes de rodar testes manuais.

## 7. Assistir aos vídeos

**Opção A – copiar para o computador.** Use o WinSCP ou o FileZilla (SFTP), ou rode no terminal **do computador**:

```bash
scp -r seuusuario@cameratrap.local:~/gravacoes .
```

Os arquivos `.mp4` abrem em qualquer player. Os `.h264` abrem no VLC.

**Opção B – pelo navegador.** No Pi, rode:

```bash
cd ~/gravacoes && python3 -m http.server 8000
```

Depois abra `http://cameratrap.local:8000` no navegador, do computador ou do celular na mesma rede. O servidor **não tem senha**: pare com `Ctrl+C` quando terminar.

## 8. Ajustes

Todos ficam em `src/cameratrap/config.py`:

| Problema | O que mudar |
|---|---|
| Muitos disparos falsos | Aumentar `MARGEM` ou `LEITURAS_PARA_DISPARAR` |
| Não detecta o animal | Diminuir `MARGEM` ou `LEITURAS_PARA_DISPARAR` |
| Vídeo começa tarde | Aumentar `SEGUNDOS_ANTES` |
| Vídeos grandes demais | Diminuir `BITRATE` ou `RESOLUCAO` |

## 9. Problemas comuns

| Sintoma | Causa provável |
|---|---|
| SSH diz "senha incorreta" | Usuário errado no comando, ou primeiro boot ainda não terminou |
| `no cameras available` | Cabo da câmera invertido ou mal encaixado |
| Sensor sempre lê o máximo | Nada atrás da área vigiada, ou o Echo não chega (confira o divisor) |
| `Device or resource busy` na câmera | O serviço já está usando a câmera |
| Vídeo de cabeça para baixo | Câmera montada invertida (gire na montagem) |
| Lente embaçada no campo | Condensação: use sílica gel dentro da caixa |
