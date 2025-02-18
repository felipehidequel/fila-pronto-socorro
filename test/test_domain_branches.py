import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from main.domain import Paciente, Risco, Atendimento, FichaAnalise, FilaAtendimento
from main.error import ValidacaoError, FilaVaziaError

class PacienteTest(unittest.TestCase):
    def test_validar_nome_valido(self):
        paciente = Paciente("Felipe Silva", "12345678900", "hidequel@email.com", "01/01/1990")
        self.assertEqual(paciente.nome, "Felipe Silva")
    
    def test_validar_nome_invalido(self):
        with self.assertRaises(ValidacaoError):
            Paciente("Artur342", "12345678900", "joaozin@email.com", "01/01/2003")
    
    def test_validar_cpf_valido(self):
        paciente = Paciente("Maria Alice", "123.456.789-00", "mali@email.com", "02/02/2003")
        self.assertEqual(paciente.cpf, "12345678900")
    
    def test_validar_cpf_invalido(self):
        with self.assertRaises(ValidacaoError):
            Paciente("Carlos Pereira", "abc123", "carlos@email.com", "05/05/1980")
    
    def test_validar_email_valido(self):
        paciente = Paciente("Ana Clara", "98765432100", "ana.clara@email.com", "10/10/1992")
        self.assertEqual(paciente.email, "ana.clara@email.com")
    
    def test_validar_email_invalido(self):
        with self.assertRaises(ValidacaoError):
            Paciente("Pedro Lima", "32165498700", "email-invalido", "12/12/1991")
    
    def test_validar_nascimento_futuro(self):
        data_futura = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        with self.assertRaises(ValidacaoError):
            Paciente("Marcos Souza", "12345678900", "marcos@email.com", data_futura)

class TestFilaAtendimento(unittest.TestCase):
    def setUp(self):
        self.fila = FilaAtendimento()

    def test_inserir_e_proximo(self):
        paciente = Mock()
        atendimento = Atendimento(paciente, Risco.VERMELHO)
        self.fila.inserir(atendimento)
        self.assertEqual(self.fila.proximo(), atendimento)
    
    def test_proximo_fila_vazia(self):
        with self.assertRaises(FilaVaziaError):
            self.fila.proximo()
    
    def test_possui_proximo(self):
        paciente = Mock()
        atendimento = Atendimento(paciente, Risco.VERMELHO)
        self.fila.inserir(atendimento)
        self.assertTrue(self.fila.possui_proximo())
    
    def test_tamanho(self):
        paciente1 = Mock()
        paciente2 = Mock()
        self.fila.inserir(Atendimento(paciente1, Risco.AMARELO))
        self.fila.inserir(Atendimento(paciente2, Risco.VERMELHO))
        self.assertEqual(self.fila.tamanho(), 2)
