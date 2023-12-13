from tussle.debate.components.answer import Answer
import abc


class AnswerRepositoryBase(metaclass=abc.ABCMeta):
    """
    This is a base class for a data repository that stores answers.
    It acts as a go-between for the API and the database or another data layer.

    This class just defines the interface and doesn't actually implement anything.
    """

    def create(self, answer: Answer) -> Answer:
        """
        Creates a brand new answer object.

        This function should assign the 'id' field to the answer.
        :return: The answer object with the 'id' field assigned.
        """
        raise NotImplementedError('AnswerRepositoryBase.create not implemented')

    def get_by_id(self, answer_id: str) -> (Answer | None):
        """
        Gets a answer by its ID.
        """
        raise NotImplementedError('AnswerRepositoryBase.get_by_id not implemented')

    def get_by_slug(self, slug: str) -> (Answer | None):
        """
        Gets a answer by its slug.
        """
        raise NotImplementedError('AnswerRepositoryBase.slug not implemented')

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the answers created for the given owner.
        """
        raise NotImplementedError('AnswerRepositoryBase.get_all_by_owner not implemented')

    def get_all(self):
        """
        Fetches all the answers in the system.
        """
        raise NotImplementedError('AnswerRepositoryBase.get_all not implemented')

    def get_all_published(self):
        """
        Fetches all the published answers found in the system.
        """
        raise NotImplementedError('AnswerRepositoryBase.get_all_published not implemented')

    def delete_by_id(self, answer_id: str):
        """
        Deletes a answer by its ID.
        """
        raise NotImplementedError('AnswerRepositoryBase.delete_by_id not implemented')

    def save(self, answer: Answer):
        """
        Saves the given answer.
        """
        raise NotImplementedError('AnswerRepositoryBase.save not implemented')

    def delete_all(self):
        """
        Deletes all the answers.
        """
        raise NotImplementedError('AnswerRepositoryBase.save not implemented')


