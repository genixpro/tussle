from tussle.articles.data_repository.article_repository_test_base import ArticleRepositoryTestBase
from .memory_article_repository import MemoryArticleRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MemoryArticleRepositoryTest(ArticleRepositoryTestBase, TussleTestCaseBase):
    def create_article_repository(self):
        return MemoryArticleRepository()

