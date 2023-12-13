from tussle.debate.data_repository.answer_repository_test_base import AnswerRepositoryTestBase
from .memory_answer_repository import MemoryAnswerRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MemoryAnswerRepositoryTest(AnswerRepositoryTestBase, TussleTestCaseBase):
    def create_answer_repository(self):
        return MemoryAnswerRepository()

