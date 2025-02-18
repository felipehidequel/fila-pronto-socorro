import unittest
from main.error import FilaVaziaError, PacienteNaoCadastradoError
from main.service import ProntoSocorroService
from main.domain import FichaAnalise, Paciente, Risco
from main.repository import AtendimentoRepository, PacienteRepository

class ProntoSocorroServiceTest(unittest.TestCase):
    def setUp(self):
        paciente_repo = PacienteRepository()
        atendimento_repo = AtendimentoRepository(paciente_repo)
        self.ps_service = ProntoSocorroService(paciente_repo, atendimento_repo)
        self.paciente = Paciente("Fulano", "11111111111", "padrao@gmail.com", "01/01/2003")
        self.paciente2 = Paciente("OutroFulano", "99999999999", "epa@gmail.com", "01/01/2003")
        super().setUp()

    def test_registrar_paciente_todos_campos_validos(self):
        saida = self.ps_service.registrar_paciente("Fulano", "11111111111", "alice@gmail.com", "01/01/2000")
        
        self.assertEqual(saida.nome, "Fulano")
        self.assertEqual(saida.cpf, "11111111111")
        self.assertEqual(saida.email, "alice@gmail.com")
        self.assertEqual(saida.nascimento, "01/01/2000")
        
    def test_classificar_risco_verde(self):
        saida = self.ps_service.classificar_risco(FichaAnalise(False, False, False, True))
        self.assertEqual(saida, Risco.VERDE)
        
    def test_insert_fila_atendimento_atendimento_nao_e_nulo(self):
        self.ps_service.registrar_paciente(self.paciente.nome, self.paciente.cpf, self.paciente.email, self.paciente.nascimento)
        atendimento = self.ps_service.registrar_atendimento(self.paciente, Risco.VERDE)
        self.assertTrue(self.ps_service.inserir_fila_atendimento(atendimento))
        
    def test_insert_fila_atendimento_atendimento_e_nulo(self):
        with self.assertRaises(AttributeError) as context:
            self.ps_service.inserir_fila_atendimento(None)
        
        self.assertIn("NoneType", str(context.exception))
        
    def test_chamar_proximo_fila_vazia(self):
        with self.assertRaises(FilaVaziaError) as context:
            self.ps_service.chamar_proximo()
        self.assertIn("Fila vazia", str(context.exception))
        
    def test_chamar_proximo_fila_com_mais_de_um_item(self):
        self.ps_service.registrar_paciente(self.paciente.nome, self.paciente.cpf, self.paciente.email, self.paciente.nascimento)
        self.ps_service.registrar_paciente(self.paciente2.nome, self.paciente2.cpf, self.paciente2.email, self.paciente2.nascimento)
        
        atendimento1 = self.ps_service.registrar_atendimento(self.paciente, Risco.VERDE)
        atendimento2 = self.ps_service.registrar_atendimento(self.paciente2, Risco.AMARELO)

        self.ps_service.inserir_fila_atendimento(atendimento1)
        self.ps_service.inserir_fila_atendimento(atendimento2)
        
        primeiro_atendimento = self.ps_service.chamar_proximo()
        
        self.assertIsNotNone(primeiro_atendimento)
        self.assertEqual(len(self.ps_service.fila_atendimento.fila), 1)
        
    def test_buscar_historico_paciente_nao_cadastrado(self):
        with self.assertRaises(PacienteNaoCadastradoError):
            self.ps_service.buscar_historico(self.paciente)


