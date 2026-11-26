"""
@file ligacoes.py
@brief Desenha docs/img/ligacoes.png (diagrama de ligações HC-SR04 + divisor + Raspberry Pi).

Uso (na pasta docs/img/fontes):  python3 ligacoes.py
Requer matplotlib.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

SAIDA = Path(__file__).resolve().parents[1] / "ligacoes.png"

fig, ax = plt.subplots(figsize=(12, 5.2), dpi=150)
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.2)
ax.axis("off")
plt.rcParams["font.family"] = "DejaVu Sans"


def caixa(x, y, w, h, cor_borda, cor_fundo, titulo):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                ec=cor_borda, fc=cor_fundo, lw=1.6))
    ax.text(x + w / 2, y + h + 0.12, titulo, ha="center", va="bottom", fontsize=12, weight="bold")


# Altura (y) de cada fio, de cima para baixo
Y = {"vcc": 4.2, "trig": 3.4, "echo": 2.6, "gnd": 1.2}
COR = {"vcc": "#D32F2F", "trig": "#1976D2", "echo": "#F9A825", "div": "#2E7D32", "gnd": "#212121"}

# ---------------- HC-SR04 ----------------
caixa(0.4, 0.8, 1.9, 3.8, "#3B6EA8", "#DDEFFF", "HC-SR04")
for nome, rot in [("vcc", "VCC"), ("trig", "Trig"), ("echo", "Echo"), ("gnd", "GND")]:
    ax.text(2.15, Y[nome], rot, ha="right", va="center", fontsize=11)
    ax.plot(2.3, Y[nome], "o", color="#333333", ms=5)

# ---------------- Raspberry Pi ----------------
caixa(8.6, 0.8, 3.0, 3.8, "#2E7D32", "#E8F5E9", "Raspberry Pi Zero W")
pinos = {"vcc": "Pino 2  —  5 V", "trig": "Pino 16  —  GPIO23",
         "echo": "Pino 18  —  GPIO24", "gnd": "Pino 6  —  GND"}
for nome, rot in pinos.items():
    ax.text(8.75, Y[nome], rot, ha="left", va="center", fontsize=11)
    ax.plot(8.6, Y[nome], "o", color="#333333", ms=5)

# ---------------- Fios diretos ----------------
for nome in ("vcc", "trig", "gnd"):
    ax.plot([2.3, 8.6], [Y[nome], Y[nome]], color=COR[nome], lw=2.6, solid_capstyle="round")

# ---------------- Echo -> R1 -> nó -> GPIO24 ;  nó -> R2 -> GND ----------------
def resistor(xc, yc, horizontal, rotulo):
    w, h = (1.0, 0.36) if horizontal else (0.36, 0.8)
    ax.add_patch(Rectangle((xc - w / 2, yc - h / 2), w, h, ec="#C98A1B", fc="#FFF4E0", lw=1.6, zorder=3))
    dx, dy = (0, 0.32) if horizontal else (0.38, 0)
    ax.text(xc + dx, yc + dy, rotulo, ha="center" if horizontal else "left", va="bottom" if horizontal else "center",
            fontsize=10.5, weight="bold", color="#8A5A00")

x_r1, x_no, x_r2 = 4.3, 5.8, 5.8
ax.plot([2.3, x_r1 - 0.5], [Y["echo"]] * 2, color=COR["echo"], lw=2.6)
resistor(x_r1, Y["echo"], True, "R1 = 1 kΩ")
ax.plot([x_r1 + 0.5, 8.6], [Y["echo"]] * 2, color=COR["div"], lw=2.6)
ax.plot(x_no, Y["echo"], "o", color=COR["div"], ms=9, zorder=4)
y_r2 = (Y["echo"] + Y["gnd"]) / 2
ax.plot([x_no, x_no], [Y["echo"], y_r2 + 0.4], color=COR["div"], lw=2.6)
resistor(x_r2, y_r2, False, "R2 = 2 kΩ")
ax.plot([x_no, x_no], [y_r2 - 0.4, Y["gnd"]], color=COR["gnd"], lw=2.6)
ax.plot(x_no, Y["gnd"], "o", color=COR["gnd"], ms=9, zorder=4)

# Anotações de tensão
ax.text(3.05, Y["echo"] + 0.15, "5 V", fontsize=9.5, color="#B26A00", ha="center", va="bottom")
ax.text(7.3, Y["echo"] + 0.15, "≈ 3,3 V", fontsize=9.5, color=COR["div"], ha="center", va="bottom")

# ---------------- Câmera ----------------
ax.add_patch(FancyBboxPatch((8.85, 0.05), 2.5, 0.5, boxstyle="round,pad=0.02,rounding_size=0.08",
                            ec="#757575", fc="#F5F5F5", lw=1.4))
ax.text(10.1, 0.3, "Câmera → conector CSI", ha="center", va="center", fontsize=10)

# ---------------- Legenda ----------------
ax.text(0.4, 0.3,
        "Divisor de tensão no Echo: 5 V × 2k / (1k + 2k) ≈ 3,3 V   •   "
        "Nunca ligue o Echo direto no GPIO",
        fontsize=9.5, color="#B5483F", va="center")

fig.tight_layout()
fig.savefig(SAIDA, bbox_inches="tight", facecolor="white")
print("Salvo em", SAIDA)
