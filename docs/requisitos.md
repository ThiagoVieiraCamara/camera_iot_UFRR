# Requisitos

## Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | O sistema deve detectar a aproximação de um animal usando o sensor HC-SR04. |
| RF02 | O sistema deve calibrar automaticamente a distância de fundo ao iniciar. |
| RF03 | O sistema deve gravar vídeo quando um animal for detectado. |
| RF04 | O vídeo deve incluir alguns segundos anteriores ao disparo (buffer circular). |
| RF05 | A gravação deve terminar quando o animal sair ou ao atingir uma duração máxima. |
| RF06 | Cada visita deve ser registrada num arquivo CSV com início, fim, duração e distância mínima. |
| RF07 | Os vídeos devem ser salvos com nome baseado na data e hora. |
| RF08 | Os vídeos devem ser convertidos para `.mp4` quando o ffmpeg estiver disponível. |
| RF09 | O sistema não deve gravar quando o espaço livre no cartão estiver abaixo do mínimo. |
| RF10 | O sistema deve iniciar automaticamente ao ligar o Raspberry Pi (serviço systemd). |

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Funcionar num Raspberry Pi Zero W (1 núcleo, 512 MB de RAM). |
| RNF02 | Operar sem monitor, com acesso apenas por SSH. |
| RNF03 | Ignorar leituras isoladas erradas do sensor (exigir leituras seguidas). |
| RNF04 | Encerrar de forma limpa ao receber Ctrl+C ou `systemctl stop`, sem corromper o vídeo em andamento. |
| RNF05 | A lógica de decisão deve ser testável sem hardware. |
| RNF06 | Todos os parâmetros ajustáveis devem ficar num único arquivo de configuração. |
| RNF07 | O código deve ser documentado no formato do Doxygen. |
