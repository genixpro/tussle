from tussle.debate.data_repository.answer_repository_test_base import AnswerRepositoryTestBase
from .fixture_answer_repository import FixtureAnswerRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.debate.components.answer import Answer


class FixtureAnswerRepositoryTest(AnswerRepositoryTestBase, TussleTestCaseBase):
    def create_answer_repository(self):
        return FixtureAnswerRepository()



    def test_load_test_case_answer(self):
        """
        This code checks that we are able to load a answer from the list of test fixtures.
        :return:
        """

        answer = self.repository.get_by_id("test_answer_1")

        self.assertIsNotNone(answer)

        self.assertIsInstance(answer, Answer)

