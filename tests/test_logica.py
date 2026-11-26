"""
@file test_logica.py
@brief Testes da calibração, do filtro de presença e da máquina de estados.
"""

import unittest

from cameratrap.logica import (
    Acao,
    Estado,
    FiltroPresenca,
    MaquinaEstados,
    calcular_calibracao,
)


class TestCalibracao(unittest.TestCase):
    def test_usa_mediana_e_ignora_leitura_maluca(self):
        cal = calcular_calibracao([0.80, 0.81, 0.79, 0.05, 0.80], margem=0.15)
        self.assertAlmostEqual(cal.fundo, 0.80)
        self.assertAlmostEqual(cal.limite, 0.65)
        self.assertAlmostEqual(cal.variacao, 0.76)

    def test_lista_vazia_da_erro(self):
        with self.assertRaises(ValueError):
            calcular_calibracao([], margem=0.15)


class TestFiltroPresenca(unittest.TestCase):
    def test_precisa_de_leituras_seguidas(self):
        f = FiltroPresenca(limite=0.65, leituras_necessarias=3)
        self.assertFalse(f.atualizar(0.40))
        self.assertFalse(f.atualizar(0.40))
        self.assertTrue(f.atualizar(0.40))

    def test_leitura_longe_zera_contagem(self):
        f = FiltroPresenca(limite=0.65, leituras_necessarias=3)
        f.atualizar(0.40)
        f.atualizar(0.40)
        self.assertFalse(f.atualizar(0.80))  # leitura "longe" no meio
        self.assertFalse(f.atualizar(0.40))
        self.assertFalse(f.atualizar(0.40))
        self.assertTrue(f.atualizar(0.40))

    def test_reiniciar(self):
        f = FiltroPresenca(limite=0.65, leituras_necessarias=2)
        f.atualizar(0.40)
        f.reiniciar()
        self.assertFalse(f.atualizar(0.40))


class TestMaquinaEstados(unittest.TestCase):
    def setUp(self):
        self.m = MaquinaEstados(segundos_depois=5, duracao_maxima=60, tempo_espera=5)

    def test_comeca_esperando(self):
        self.assertIs(self.m.estado, Estado.ESPERANDO)
        self.assertIs(self.m.atualizar(0, presente=False), Acao.NENHUMA)

    def test_inicia_quando_ha_presenca(self):
        self.assertIs(self.m.atualizar(0, presente=True), Acao.INICIAR_GRAVACAO)
        self.assertTrue(self.m.gravando)

    def test_para_depois_que_o_animal_sai(self):
        self.m.atualizar(0, True)
        self.m.atualizar(2, True)                      # ainda presente aos 2 s
        self.assertIs(self.m.atualizar(6, False), Acao.NENHUMA)  # só 4 s ausente
        self.assertIs(self.m.atualizar(7, False), Acao.PARAR_GRAVACAO)
        self.assertFalse(self.m.gravando)

    def test_para_na_duracao_maxima_mesmo_com_presenca(self):
        self.m.atualizar(0, True)
        self.assertIs(self.m.atualizar(59, True), Acao.NENHUMA)
        self.assertIs(self.m.atualizar(60, True), Acao.PARAR_GRAVACAO)

    def test_respeita_tempo_de_espera(self):
        self.m.atualizar(0, True)
        self.m.atualizar(5, False)                     # para aos 5 s
        self.assertIs(self.m.atualizar(7, True), Acao.NENHUMA)   # ainda na espera
        self.assertIs(self.m.atualizar(10, True), Acao.INICIAR_GRAVACAO)

    def test_cancelar_volta_a_esperar(self):
        self.m.atualizar(0, True)
        self.m.cancelar(0, esperar=60)
        self.assertFalse(self.m.gravando)
        self.assertIs(self.m.atualizar(30, True), Acao.NENHUMA)
        self.assertIs(self.m.atualizar(60, True), Acao.INICIAR_GRAVACAO)


if __name__ == "__main__":
    unittest.main()
