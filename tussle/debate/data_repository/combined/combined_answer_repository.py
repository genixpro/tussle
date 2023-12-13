from tussle.debate.data_repository.memory.memory_answer_repository import MemoryAnswerRepository
from tussle.debate.components.answer import Answer
from tussle.debate.data_repository.answer_repository_base import AnswerRepositoryBase
import pkg_resources


class CombinedAnswerRepository(AnswerRepositoryBase):
    """
    This is a data repository that combines together other data repositories.
    It has a main repository which is where data is saved and loaded from.
    But it has a secondary function where it will load things from the
    fallback repositories if it can.
    """

    def __init__(self, primary_repository: AnswerRepositoryBase, fallback_repositories: list[AnswerRepositoryBase]):
        self.primary_repository = primary_repository
        self.fallback_repositories = fallback_repositories

    def get_by_id(self, answer_id: str):
        """
        Gets a answer by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the primary repository.
        answer = self.primary_repository.get_by_id(answer_id)
        if answer:
            return answer

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            answer = fallback_repository.get_by_id(answer_id)
            if answer:
                # Save it into the primary repository
                self.primary_repository.save(answer)
                return answer

        return None

    def get_by_slug(self, slug: str) -> (Answer | None):
        """
        Gets an answer by its slug.
        """
        # First attempt to get it from the primary repository.
        answer = self.primary_repository.get_by_slug(slug)
        if answer:
            return answer

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            answer = fallback_repository.get_by_slug(slug)
            if answer:
                # Save it into the primary repository
                self.primary_repository.save(answer)
                return answer

        return None

    def create(self, answer: Answer):
        """
        Creates a brand new answer object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The answer object with the 'id' field assigned.
        """
        return self.primary_repository.create(answer)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the answers created for the given owner.
        """
        return self.primary_repository.get_all_by_owner(owner)

    def get_all(self):
        """
        Fetches all the answers created for the given owner.
        """
        return self.primary_repository.get_all()

    def get_all_published(self):
        """
        Fetches all the published answers found in the system.
        """
        return self.primary_repository.get_all_published()

    def delete_by_id(self, answer_id: str):
        """
        Deletes a answer by its ID.
        """
        return self.primary_repository.delete_by_id(answer_id)

    def save(self, answer: Answer):
        """
        Saves the given answer.
        """
        return self.primary_repository.save(answer)

    def delete_all(self):
        """
        Deletes all the answers.
        """
        return self.primary_repository.delete_all()
