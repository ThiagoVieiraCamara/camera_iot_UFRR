# Revisão comparativa da literatura

Esta seção compara o projeto com **quatro trabalhos acadêmicos** sobre armadilhas fotográficas (*camera traps*) e sobre o uso do Raspberry Pi em pesquisa biológica. Ela traz:

1. **Pontos em comum** entre os trabalhos analisados.
2. **Principais diferenças** entre as abordagens.
3. **Comparação dos métodos de disparo**, que é o ponto central deste projeto.

Identificação dos trabalhos:

* **A1** – *WiseEye* (Nazir et al., 2017): plataforma de camera trap programável baseada em Raspberry Pi
* **A2** – *PICT* (Droissart et al., 2021): camera trap de baixo custo com Raspberry Pi Zero para estudar interações planta–inseto
* **A3** – *HALT* (Hobbs & Brehme, 2017): camera trap com gatilho ativo para anfíbios, répteis, pequenos mamíferos e invertebrados
* **A4** – Jolles (2021): revisão e guia sobre aplicações do Raspberry Pi em biologia

As referências completas estão no fim do documento.

---

## 🔹 Tabela 1 — Pontos em comum

| Ponto em comum | Descrição |
| :--- | :--- |
| **Monitoramento sem observador humano** | Todos tratam de registrar animais sem uma pessoa presente, o que reduz a interferência no comportamento. |
| **Limitações das câmeras comerciais** | A1, A2 e A3 partem de problemas das camera traps comerciais: pouca flexibilidade, disparos falsos e falhas com animais pequenos. |
| **Hardware de baixo custo e aberto** | A1, A2 e A4 usam o Raspberry Pi. A3 modifica câmeras comerciais com um circuito próprio. |
| **Gatilho como ponto crítico** | Todos discutem quando e como a câmera deve disparar: sensor, sensibilidade, falsos positivos e falsos negativos. |
| **Software configurável** | A1, A2 e A4 destacam poder ajustar resolução, taxa de quadros, tempos e comportamento por software. |
| **Validação prática** | A1, A2 e A3 testam protótipos em condições reais ou comparam com equipamentos comerciais. |
| **Caráter acadêmico** | Todos são publicações científicas revisadas por pares, com foco em pesquisa ecológica. |

**Fontes:** A1, A2, A3 e A4

---

## 🔹 Tabela 2 — Diferenças entre os trabalhos

| Trabalho | Objetivo principal | Diferencial | Foco |
| :--- | :--- | :--- | :--- |
| **A1** | Camera trap flexível e expansível para pesquisa de fauna | *Confirmatory sensing*: o disparo do PIR é confirmado por outro sensor (radar ou mudança de pixels) para reduzir falsos positivos | Programabilidade e redução de imagens inúteis |
| **A2** | Filmar interações planta–inseto a baixo custo (< 100 USD) | Filmagem **contínua** (sem gatilho), iluminação infravermelha automática, controle remoto por Wi-Fi | Insetos e polinização em campo |
| **A3** | Detectar animais que o PIR não percebe bem | Gatilho **ativo** (HALT) acoplado a câmeras comerciais, para trilhas estreitas e túneis | Ectotérmicos e pequenos mamíferos |
| **A4** | Mapear e incentivar o uso do Raspberry Pi em biologia | Revisão de mais de cem estudos, com guias passo a passo | Panorama e boas práticas |
| **Este projeto** | Camera trap didática e de baixo custo com Raspberry Pi Zero W | Gatilho **ativo por distância** (ultrassom) com calibração automática e **buffer pré-disparo** | Sistemas embarcados e observação de animais num ponto fixo |

---

## 🔹 Tabela 3 — Métodos de disparo

| Método | Usado em | Como detecta | Vantagens | Limitações |
| :--- | :--- | :--- | :--- | :--- |
| **PIR (infravermelho passivo)** | Câmeras comerciais; base do A1 | Variação rápida de calor no campo de visão | Padrão de mercado; baixo consumo | Precisa que o animal seja mais quente que o ambiente e se mova. Falha com ectotérmicos e animais pequenos (A3). |
| **PIR + confirmação** | A1 | PIR confirmado por radar ou por análise de imagem | Menos falsos positivos e negativos que uma câmera comercial | Mais complexo e caro |
| **Gatilho ativo (HALT)** | A3 | O sistema emite um sinal e detecta a interrupção | Não depende de calor; detecta animais pequenos e de sangue frio | Área de detecção estreita (trilha, túnel) |
| **Filmagem contínua** | A2 | Não há gatilho: grava o tempo todo | Nunca perde um evento | Muito mais armazenamento e energia. Exige revisar horas de vídeo. |
| **Ultrassom por distância** | **Este projeto** | Mede a distância até o fundo calibrado e dispara quando algo fica mais perto | Não depende de calor; barato; com o buffer, o vídeo inclui o momento da chegada | Cone estreito (~15°). Pelos e penas refletem pouco som. O pulso de 40 kHz é **audível para vários mamíferos**. |

---

## 🔹 Interpretação

* Todos os trabalhos concordam que **o gatilho é o ponto fraco das camera traps**. Cada um ataca o problema de um jeito:
  * **A1** confirma o PIR com um segundo sensor.
  * **A2** elimina o gatilho e filma tudo.
  * **A3** troca o PIR por um gatilho ativo.
  * **A4** mostra que o Raspberry Pi tornou esse tipo de solução acessível a pesquisadores.
* **Posição deste projeto:** ele usa um gatilho ativo, como o A3, só que por medição de distância com ultrassom. Por isso, em princípio, a detecção não depende da temperatura do animal. Do A2 vem a mesma plataforma de baixo custo (Raspberry Pi Zero com Wi-Fi). O **buffer circular** é um meio-termo entre o A2 e as câmeras com gatilho: guarda os segundos anteriores ao disparo sem gravar o tempo todo no cartão.
* **Lição para evolução:** o conceito de *confirmatory sensing* do A1 indica um caminho natural para este projeto. Seria combinar o ultrassom com um sensor PIR ou com análise de imagem, para reduzir disparos falsos.

---

## 🔹 Referências

**A1** — NAZIR, S.; NEWEY, S.; IRVINE, R. J.; VERDICCHIO, F.; DAVIDSON, P.; FAIRHURST, G.; VAN DER WAL, R. WiseEye: Next Generation Expandable and Programmable Camera Trap Platform for Wildlife Research. *PLoS ONE*, v. 12, n. 1, e0169758, 2017. DOI: [10.1371/journal.pone.0169758](https://doi.org/10.1371/journal.pone.0169758)

**A2** — DROISSART, V.; AZANDI, L.; ONGUENE, E. R.; SAVIGNAC, M.; SMITH, T. B.; DEBLAUWE, V. PICT: A low-cost, modular, open-source camera trap system to study plant–insect interactions. *Methods in Ecology and Evolution*, v. 12, n. 8, p. 1389–1396, 2021. DOI: [10.1111/2041-210X.13618](https://doi.org/10.1111/2041-210X.13618)

**A3** — HOBBS, M. T.; BREHME, C. S. An improved camera trap for amphibians, reptiles, small mammals, and large invertebrates. *PLoS ONE*, v. 12, n. 10, e0185026, 2017. DOI: [10.1371/journal.pone.0185026](https://doi.org/10.1371/journal.pone.0185026)

**A4** — JOLLES, J. W. Broad-scale applications of the Raspberry Pi: A review and guide for biologists. *Methods in Ecology and Evolution*, v. 12, n. 9, p. 1562–1579, 2021. DOI: [10.1111/2041-210X.13652](https://doi.org/10.1111/2041-210X.13652)

**Complementar** — WELBOURNE, D. J.; CLARIDGE, A. W.; PAULL, D. J.; LAMBERT, A. How do passive infrared triggered camera traps operate and why does it matter? Breaking down common misconceptions. *Remote Sensing in Ecology and Conservation*, v. 2, n. 2, p. 77–83, 2016.
