from tussle.debate.data_repository.answer_repository_test_base import AnswerRepositoryTestBase
from .mongo_answer_repository import MongoAnswerRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MongoAnswerRepositoryTest(AnswerRepositoryTestBase, TussleTestCaseBase):
    def create_answer_repository(self):
        return MongoAnswerRepository(
            mongo_db_connection=self.container.mongo_db_connection(),
        )

