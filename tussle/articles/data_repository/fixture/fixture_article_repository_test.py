from tussle.articles.data_repository.article_repository_test_base import ArticleRepositoryTestBase
from .fixture_article_repository import FixtureArticleRepository
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from tussle.articles.components.article import Article


class FixtureArticleRepositoryTest(ArticleRepositoryTestBase, ArticulonTestCaseBase):
    def create_article_repository(self):
        return FixtureArticleRepository()



    def test_load_test_case_article(self):
        """
        This code checks that we are able to load a article from the list of test fixtures.
        :return:
        """

        article = self.repository.get_by_id("test_article_1")

        self.assertIsNotNone(article)

        self.assertIsInstance(article, Article)

