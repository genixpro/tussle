from tussle.debate.data_repository.answer_repository_test_base import AnswerRepositoryTestBase
from tussle.debate.data_repository.memory.memory_answer_repository import MemoryAnswerRepository
from .combined_answer_repository import CombinedAnswerRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.debate.components.answer import Answer
import pkg_resources


class CombinedAnswerRepositoryTest(AnswerRepositoryTestBase, TussleTestCaseBase):
    def create_answer_repository(self):
        self.primary = MemoryAnswerRepository()
        self.fallback1 = MemoryAnswerRepository()
        self.fallback2 = MemoryAnswerRepository()

        return CombinedAnswerRepository(
            primary_repository=self.primary,
            fallback_repositories=[
                self.fallback1,
                self.fallback2,
            ]
        )

    def test_load_fallback(self):
        """
        This code checks that we are able to load a answer from the list of test fixtures.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"answers/test_fixtures/test_answer_1.json").decode("utf-8")
        answer = Answer.from_json(data_str)
        answer.id = "new_test_id"

        # Check that we can't load the answer initially
        loaded_answer = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_answer)

        # Save the answer into the fallback repository.
        self.fallback1.save(answer)

        # Now try to load it from the combined repository.
        loaded_answer = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(answer)
        self.assertEqual(loaded_answer, answer)

    def test_load_second_fallback(self):
        """
        This code checks that if you have multiple fallbacks, you can still load data from the second fallbacks.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"answers/test_fixtures/test_answer_1.json").decode("utf-8")
        answer = Answer.from_json(data_str)
        answer.id = "new_test_id"

        # Check that we can't load the answer initially
        loaded_answer = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_answer)

        # Save the answer into the second fallback repository.
        self.fallback2.save(answer)

        # Now try to load it from the combined repository.
        loaded_answer = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(answer)
        self.assertEqual(loaded_answer, answer)
