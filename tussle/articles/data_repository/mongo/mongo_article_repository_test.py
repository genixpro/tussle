from tussle.articles.data_repository.article_repository_test_base import ArticleRepositoryTestBase
from .mongo_article_repository import MongoArticleRepository
from tussle.general.testing.test_case_base import ArticulonTestCaseBase


class MongoArticleRepositoryTest(ArticleRepositoryTestBase, ArticulonTestCaseBase):
    def create_article_repository(self):
        return MongoArticleRepository(
            mongo_db_connection=self.container.mongo_db_connection(),
        )

