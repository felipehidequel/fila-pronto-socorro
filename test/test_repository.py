import unittest
from main.repository import PacienteRepository, AtendimentoRepository
from main.domain import Paciente, Atendimento, Risco
from main.error import PacienteNaoCadastradoError

class PacienteRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.paciente_repo = PacienteRepository()
        super().setUp()

    def test_inserir_objeto(self):
        self.paciente_repo.inserir(Paciente("Fulano", "11111111111", "padrao@gmail.com", "01/01/2003"))
        self.assertEqual(len(self.paciente_repo.pacientes), 1)

    def test_inserir_nulo(self):
        self.paciente_repo.inserir(None)
        self.assertEqual(len(self.paciente_repo.pacientes), 0)

    def test_buscar_nao_encontrado(self):
        buscar = self.paciente_repo.buscar("11111111311")
        self.assertIsNone(buscar)

    def test_buscar_encontrado(self):
        self.paciente_repo.inserir(Paciente("FulanoDois", "11111111311", "outro@gmail.com", "01/01/2003"))
        buscar = self.paciente_repo.buscar("11111111311")
        self.assertEqual(buscar.nome, "FulanoDois")


class AtendimentoRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.paciente_repo = PacienteRepository()
        self.atendimento_repo = AtendimentoRepository(self.paciente_repo)
        self.paciente = Paciente("FlaFlu", "21111111311", "zap@gmail.com", "01/01/2003")
        super().setUp()

    def test_inserir_paciente_nao_cadastrado(self):
        with self.assertRaises(PacienteNaoCadastradoError):
            self.atendimento_repo.inserir(Atendimento(self.paciente, Risco.VERDE))
        self.assertEqual(len(self.atendimento_repo.atendimentos), 0)

    def test_historico_atendimentos_paciente_cadastrado_com_mais_de_uma_consulta(self):
        p = Paciente("PorAi", "11115431311", "ts@gmail.com", "01/01/2003")
        self.paciente_repo.inserir(p)
        self.atendimento_repo.inserir(Atendimento(p, Risco.VERDE))
        self.atendimento_repo.inserir(Atendimento(p, Risco.VERDE))
        self.atendimento_repo.inserir(Atendimento(p, Risco.VERDE))
        self.atendimento_repo.inserir(Atendimento(p, Risco.VERMELHO))
        self.assertEqual(len(self.atendimento_repo.historico_atendimentos("11115431311")), 4)

    def test_historico_atendimentos_paciente_cadastrado_com_nenhuma_consulta(self):
        p = Paciente("PorAi", "11115431311", "ts@gmail.com", "01/01/2003")
        self.paciente_repo.inserir(p)
        self.assertEqual(len(self.atendimento_repo.historico_atendimentos("11115431311")), 0)

    def test_historico_atendimentos_paciente_nao_cadastrado(self):
        with self.assertRaises(PacienteNaoCadastradoError) as context:
            self.atendimento_repo.historico_atendimentos("11115431311")
        self.assertIn('Paciente não cadastrado', str(context.exception))
        self.assertEqual(len(self.atendimento_repo.atendimentos), 0)
