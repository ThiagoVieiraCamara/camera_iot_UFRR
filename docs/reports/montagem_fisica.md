# Montagem física e posicionamento

## 1. Posicionamento do sensor

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


---

## 2. Câmera

| Item | Recomendação |
| :--- | :--- |
| Cabo | Cabo próprio para Pi Zero 2 W (ponta estreita), com os contatos virados para a placa |
| Foco | Camera OV5647 |
| Orientação | Se ficar de cabeça para baixo, use `--rotation 180` nos testes com `rpicam-vid` |

---

## 3. Alimentação

| Opção | Observação |
| :--- | :--- |
| Conexão USB raspberry pi zero 2 W com o computador | Mais simples para testes |

---

## 4. Lista de materiais

| Item | Qtd. | Custo aproximado (R$) |
| :--- | :---: | :---: |
| Raspberry Pi Zero 2 W | 1 | R$ 800 |
| Módulo de câmera + cabo para Pi Zero 2 W | 1 | R$ 70 |
| Sensor HC-SR04 | 1 | R$ 18 |
| Resistores 1 kΩ e 2 kΩ | 1 de cada | R$ 7 |
| Cartão microSD | 1 | R$ 55 |
| **Total** | | R$ 950 |
