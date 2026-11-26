# 🧰 Montagem física e posicionamento

> **[Preencher]** Este documento traz as decisões técnicas de montagem. Complete com a sua montagem real: fotos, medidas e, se houver, os modelos 3D da caixa. Coloque as imagens em `docs/img/montagem/`.

## 1. Caixa (invólucro)

O invólucro deve proteger o Raspberry Pi, a câmera e o sensor no local de observação.

| Requisito | Motivo |
| :--- | :--- |
| Caixa vedada, com janela de vidro ou acrílico na frente da lente | Proteção contra chuva e poeira sem bloquear a imagem |
| As duas cápsulas do HC-SR04 **livres** (fora do vidro) | Vidro ou acrílico refletem o ultrassom, e o sensor passaria a medir a própria caixa |
| Sílica gel dentro da caixa | Evita condensação na lente |
| Entrada vedada para o cabo de energia | Alimentação externa (powerbank ou fonte) |

**[Preencher]** Material e dimensões da caixa usada, foto externa e foto interna.

**[Preencher, se houver]** Modelo 3D (Tinkercad, Fusion etc.): imagens em `docs/img/montagem/` e arquivos STL numa pasta `stl/`.

---

## 2. Posicionamento do sensor

O HC-SR04 tem um **cone de detecção estreito**, de cerca de 15°. Considerando 15° como abertura total, a largura aproximada da área "vista" pelo sensor é:

| Distância do sensor | Largura aproximada do cone |
| :---: | :---: |
| 0,25 m | ≈ 7 cm |
| 0,50 m | ≈ 13 cm |
| 1,00 m | ≈ 26 cm |
| 2,00 m | ≈ 53 cm |

*Cálculo: largura ≈ 2 × d × tan(7,5°) ≈ 0,26 × d.*

Recomendações:

1. **Aponte para um ponto de passagem obrigatória**, como a entrada de um comedouro, bebedouro, toca ou poleiro. O sensor vigia uma faixa estreita, não uma área ampla.
2. **Tenha um fundo fixo** atrás da área vigiada (parede, chão inclinado, fundo do comedouro), dentro de 2 m. Sem fundo, o sensor lê o máximo, e a calibração avisa isso.
3. **De preferência a menos de 1 m do animal.** Alvos pequenos e com pelo ou penas refletem pouco som. A folha de dados recomenda alvos de pelo menos 0,5 m² para melhor resultado, e animais são bem menores que isso.
4. **Câmera ao lado do sensor, mirando a mesma região.** O campo de visão da câmera é muito mais largo que o cone do sensor, então o animal aparece na imagem antes de disparar o sensor. O buffer pré-disparo de 3 s registra essa chegada.
5. **Proteja o sensor de chuva**, que pode causar leituras falsas, ou use a versão à prova d'água JSN-SR04T.

**[Preencher]** Altura do sensor, distância até o fundo, ângulo usado e foto do posicionamento.

---

## 3. Câmera

| Item | Recomendação |
| :--- | :--- |
| Cabo | Cabo próprio para Pi Zero (ponta estreita), com os contatos virados para a placa |
| Foco | Camera Module 3: foco automático. Camera Module v2: foco fixo, pode precisar de ajuste para perto. |
| Noite | Versão NoIR com LEDs infravermelhos de 850 nm. Teste se os LEDs não interferem no sensor. |
| Orientação | Se ficar de cabeça para baixo, use `--rotation 180` nos testes com `rpicam-vid` |

**[Preencher]** Modelo de câmera usado e exemplos de quadros gravados (`docs/img/registros/`).

---

## 4. Alimentação

| Opção | Observação |
| :--- | :--- |
| Fonte 5 V da tomada | Mais simples para testes |
| Powerbank | Autonomia de 1 a 2 dias, dependendo da capacidade |
| Painel solar + bateria | Para uso prolongado em campo |

**[Preencher]** Fonte usada e autonomia medida.

---

## 5. Lista de materiais

| Item | Qtd. | Custo aproximado (R$) |
| :--- | :---: | :---: |
| Raspberry Pi Zero W | 1 | **[Preencher]** |
| Módulo de câmera + cabo para Pi Zero | 1 | **[Preencher]** |
| Sensor HC-SR04 | 1 | **[Preencher]** |
| Resistores 1 kΩ e 2 kΩ | 1 de cada | **[Preencher]** |
| Cartão microSD | 1 | **[Preencher]** |
| Fonte / powerbank | 1 | **[Preencher]** |
| Caixa e fixação | 1 | **[Preencher]** |
| **Total** | | **[Preencher]** |
