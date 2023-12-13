from tussle.debate.data_repository.answer_repository_base import AnswerRepositoryBase
from tussle.debate.components.answer import Answer


class MemoryAnswerRepository(AnswerRepositoryBase):
    """
    This is a simple repository for answers which just store them in memory.

    Chiefly useful for testing.
    """

    def __init__(self):
        self.id_counter = 0
        self.answers = {}

    def create(self, answer: Answer):
        """
        Creates a brand new answer object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The answer object with the 'id' field assigned.
        """
        if answer.id is None:
            answer.id = f"answer-{self.id_counter}"
        self.id_counter += 1

        self.answers[answer.id] = answer
        return answer

    def get_by_id(self, answer_id: str):
        """
        Gets a answer by its ID.
        """
        return self.answers.get(answer_id)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the answers created for the given owner.
        """
        return [answer for answer in self.answers.values() if answer.owner == owner]

    def get_all(self):
        """
        Fetches all the answers in the system.
        """
        return [answer for answer in self.answers.values()]

    def delete_by_id(self, answer_id: str):
        """
        Deletes a answer by its ID.
        """
        del self.answers[answer_id]

    def save(self, answer: Answer):
        """
        Saves the given answer.
        """
        self.answers[answer.id] = answer

    def delete_all(self):
        """
        Deletes all the answers.
        """
        self.answers = {}
