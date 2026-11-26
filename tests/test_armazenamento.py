"""
@file test_armazenamento.py
@brief Testes dos nomes de arquivo e do log CSV.
"""

import csv
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from cameratrap.armazenamento import CABECALHO_CSV, nome_do_video, registrar_visita


class TestNomeDoVideo(unittest.TestCase):
    def test_formato(self):
        p = nome_do_video(Path("/tmp"), datetime(2026, 11, 26, 13, 5, 9))
        self.assertEqual(p.name, "2026-11-26_13-05-09.h264")


class TestRegistrarVisita(unittest.TestCase):
    def test_cria_cabecalho_uma_vez_e_acrescenta_linhas(self):
        with tempfile.TemporaryDirectory() as pasta:
            log = Path(pasta) / "visitas.csv"
            ini = datetime(2026, 11, 26, 6, 0, 0)
            fim = datetime(2026, 11, 26, 6, 0, 12, 500000)
            registrar_visita(log, ini, fim, 0.423, "a.mp4")
            registrar_visita(log, ini, fim, 0.3, "b.mp4")

            with log.open(encoding="utf-8") as f:
                linhas = list(csv.reader(f))

        self.assertEqual(linhas[0], CABECALHO_CSV)
        self.assertEqual(len(linhas), 3)
        self.assertEqual(
            linhas[1],
            ["2026-11-26T06:00:00", "2026-11-26T06:00:12", "12.5", "42.3", "a.mp4"],
        )


if __name__ == "__main__":
    unittest.main()
