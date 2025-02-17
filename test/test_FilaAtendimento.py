import unittest
import heapq
from main.domain import FilaAtendimento, Risco, Atendimento, Paciente
from main.error import FilaVaziaError

class TestFilaAtendimento(unittest.TestCase):
    def setUp(self):
        self.fila = FilaAtendimento()
        self.paciente = Paciente(nome="Teste", cpf="12345678900", email="teste@teste.com", nascimento="01/01/2000")

    def test_RT1_insercao_risco_vermelho(self):
        atendimento = Atendimento(self.paciente, Risco.VERMELHO)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_RT2_insercao_risco_amarelo(self):
        atendimento = Atendimento(self.paciente, Risco.AMARELO)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_RT3_insercao_risco_laranja(self):
        atendimento = Atendimento(self.paciente, Risco.LARANJA)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_RT4_insercao_risco_azul(self):
        atendimento = Atendimento(self.paciente, Risco.AZUL)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_RT5_proximo_nao_existe(self):
        atendimento = Atendimento(self.paciente, Risco.VERDE)
        self.fila.inserir(atendimento)
        self.fila.proximo()
        with self.assertRaises(FilaVaziaError):
            self.fila.proximo()

    def test_RT6_proximo_existe_apos_retirada(self):
        atendimento1 = Atendimento(self.paciente, Risco.VERDE)
        atendimento2 = Atendimento(self.paciente, Risco.AMARELO)
        self.fila.inserir(atendimento1)
        self.fila.inserir(atendimento2)
        self.fila.proximo()
        self.assertTrue(self.fila.possui_proximo())

    def test_RT7_tamanho_igual_a_um(self):
        atendimento = Atendimento(self.paciente, Risco.VERDE)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.tamanho(), 1)

    def test_RT8_tamanho_igual_a_zero(self):
        self.assertEqual(self.fila.tamanho(), 0)