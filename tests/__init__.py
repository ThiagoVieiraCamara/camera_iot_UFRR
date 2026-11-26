"""
@file tests/__init__.py
@brief Testes que rodam no computador, sem Raspberry Pi.

Adiciona a pasta `src/` ao caminho de importação para os testes
encontrarem o pacote `cameratrap`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
