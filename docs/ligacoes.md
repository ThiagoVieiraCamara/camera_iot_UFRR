# Ligações elétricas

## Sensor HC-SR04

| HC-SR04 | Raspberry Pi Zero W | Observação |
|---|---|---|
| VCC | Pino 2 (5 V) | |
| GND | Pino 6 (GND) | |
| Trig | Pino 16 (GPIO23) | Ligação direta (3,3 V é suficiente para disparar) |
| Echo | Pino 18 (GPIO24) | **Obrigatório passar pelo divisor de tensão** |

### Por que o divisor de tensão?

O HC-SR04 funciona em 5 V, e o pino **Echo** devolve um pulso de 5 V. Os GPIOs do Raspberry Pi aguentam no máximo **3,3 V**. Ligar o Echo direto pode queimar o pino ou a placa.

O divisor reduz os 5 V para cerca de 3,3 V:

```
 Echo (HC-SR04) ──[ R1 = 1 kΩ ]──┬──── Pino 18 (GPIO24)
                                 │
                            [ R2 = 2 kΩ ]
                                 │
 GND ────────────────────────────┴──── Pino 6 (GND)

 Tensão no GPIO = 5 V × 2k / (1k + 2k) ≈ 3,3 V
```

Se não tiver um resistor de 2 kΩ, use dois de 1 kΩ em série.

**Exceção:** o **HC-SR04P** e o **RCWL-1601** funcionam em 3,3 V. Com eles, alimente o sensor pelo pino 1 (3,3 V) e dispense o divisor.

## Câmera

- Use o cabo **próprio para Pi Zero**. A ponta do lado do Pi é mais estreita que nas outras placas.
- Os contatos metálicos do cabo ficam virados **para a placa**.
- Teste com: `rpicam-still -o teste.jpg`

## Referência dos pinos usados

```
           3V3  (1) (2)  5V    ← VCC do HC-SR04
                (3) (4)
                (5) (6)  GND   ← GND do HC-SR04 e do divisor
                 ...
                (15)(16) GPIO23 ← Trig
                (17)(18) GPIO24 ← Echo (pelo divisor)
```

Para mudar os pinos, edite `PINO_TRIG` e `PINO_ECHO` em `src/cameratrap/config.py`.

## Limitações do sensor

- **Alcance:** de 2 cm a cerca de 2–4 m, num cone estreito de uns 15°. Funciona melhor com o animal a menos de 1 m e de frente para o sensor.
- **Pelos e penas** absorvem o ultrassom, então animais pequenos podem refletir pouco eco.
- **Muitos mamíferos ouvem o ultrassom de 40 kHz**, como ratos, morcegos, gatos e cães. Observe se eles evitam o local. Aves geralmente não ouvem nessa frequência.
- O sensor **não é à prova d'água**. Para uso exposto à chuva, uma alternativa é o JSN-SR04T, que funciona do mesmo jeito.
- O ideal é ter uma superfície fixa atrás da área vigiada, como uma parede, o chão ou o fundo de um comedouro.
