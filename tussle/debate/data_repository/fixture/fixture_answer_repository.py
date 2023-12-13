from tussle.debate.data_repository.memory.memory_answer_repository import MemoryAnswerRepository
from tussle.debate.components.answer import Answer
import pkg_resources

class FixtureAnswerRepository(MemoryAnswerRepository):
    """
    This is a simple repository for bulk chart evaluations which just store them in memory.

    Chiefly useful for testing.
    """

    def get_by_id(self, answer_id: str):
        """
        Gets a answer by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the super class, the memory repository.
        answer = super().get_by_id(answer_id)
        if answer:
            return answer

        # Now attempt to load it from a fixture file.
        answer = self._load_from_fixture(answer_id)

        return answer

    def _load_from_fixture(self, id):
        try:
            data_str = pkg_resources.resource_string("tussle", f"answers/test_fixtures/{id}.json").decode("utf-8")
        except FileNotFoundError:
            return None

            data_str = pkg_resources.resource_string("tussle", f"answers/test_fixtures/{id}.json").decode("utf-8")
        obj = Answer.from_json(data_str)
        return obj
