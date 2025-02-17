import unittest
from datetime import datetime
from main.error import ValidacaoError
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento


class EntitiesTest(unittest.TestCase):
    def test_nome_pessoa_validate(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="   ", cpf="11111111111", email = "teste@teste.com", nascimento="11/11/1111")
        self.assertIn("nome", context.exception.message)

    def test_cpf_pessoa_validar(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="muito massa", cpf=" ", email = "teste@teste.com", nascimento="11/11/1111")
        self.assertIn("CPF", context.exception.message)

    def test_email_pessoa_validar(self):
        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="muito massa", cpf="11111111111", email = "", nascimento="11/11/1111")
        self.assertIn("E-mail", context.exception.message)

    def test_nascimento_pessoa_validar(self):
        with self.assertRaises(ValueError) as context:
            Paciente(nome="muito massa", cpf="11111111111", email = "teste@teste.com", nascimento=" ")
        self.assertIn("nascimento", context.exception.message)

    def test_pessoa_validar(self):
        p = Paciente(nome="Felipe", cpf="11111111111", email = "teste@teste.com", nascimento="11/11/1111")
    
    
