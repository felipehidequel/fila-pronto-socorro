import unittest
from unittest.mock import Mock
from main.domain import Paciente, FichaAnalise, Risco, Atendimento
from main.repository import PacienteRepository, AtendimentoRepository
from main.service import ProntoSocorroService

class ProntoSocorroServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.pacientes_mock = Mock(spec=PacienteRepository)
        self.atendimentos_mock = Mock(spec=AtendimentoRepository)
        self.service = ProntoSocorroService(self.pacientes_mock, self.atendimentos_mock)

    def test_registrar_paciente(self):
        paciente = self.service.registrar_paciente("João", "12345678900", "joao@email.com", "01/01/1980")
        self.pacientes_mock.inserir.assert_called_once()
        self.assertEqual(paciente.nome, "João")
        self.assertEqual(paciente.cpf, "12345678900")

    def test_classificar_risco_vermelho(self):
        ficha = FichaAnalise(risco_morte=True, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.service.classificar_risco(ficha), Risco.VERMELHO)
    
    def test_classificar_risco_amarelo(self):
        ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.service.classificar_risco(ficha), Risco.AMARELO)
    
    def test_classificar_risco_laranja(self):
        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=True, gravidade_baixa=False)
        self.assertEqual(self.service.classificar_risco(ficha), Risco.LARANJA)
    
    def test_classificar_risco_verde(self):
        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=True)
        self.assertEqual(self.service.classificar_risco(ficha), Risco.VERDE)
    
    def test_classificar_risco_azul(self):
        ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
        self.assertEqual(self.service.classificar_risco(ficha), Risco.AZUL)

    def test_registrar_atendimento(self):
        paciente = Mock(spec=Paciente)
        atendimento = self.service.registrar_atendimento(paciente, Risco.VERMELHO)
        self.atendimentos_mock.inserir.assert_called_once()
        self.assertEqual(atendimento.risco, Risco.VERMELHO)
    
    def test_chamar_proximo(self):
        atendimento_mock = Mock(spec=Atendimento)
        self.service.fila_atendimento.proximo = Mock(return_value=atendimento_mock)
        self.assertEqual(self.service.chamar_proximo(), atendimento_mock)
    
    def test_buscar_historico(self):
        paciente = Mock(spec=Paciente)
        paciente.cpf = "12345678900"
        self.service.atendimentos.historico_atendimentos = Mock(return_value=[Mock(spec=Atendimento)])
        historico = self.service.buscar_historico(paciente)
        self.service.atendimentos.historico_atendimentos.assert_called_with("12345678900")
        self.assertEqual(len(historico), 1)