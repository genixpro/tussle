from tussle.articles.data_repository.article_repository_test_base import ArticleRepositoryTestBase
from .mongo_article_repository import MongoArticleRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MongoArticleRepositoryTest(ArticleRepositoryTestBase, TussleTestCaseBase):
    def create_article_repository(self):
        return MongoArticleRepository(
            mongo_db_connection=self.container.mongo_db_connection(),
        )

