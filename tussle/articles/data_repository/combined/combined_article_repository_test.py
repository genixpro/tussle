from tussle.articles.data_repository.article_repository_test_base import ArticleRepositoryTestBase
from tussle.articles.data_repository.memory.memory_article_repository import MemoryArticleRepository
from .combined_article_repository import CombinedArticleRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.articles.components.article import Article
import pkg_resources


class CombinedArticleRepositoryTest(ArticleRepositoryTestBase, TussleTestCaseBase):
    def create_article_repository(self):
        self.primary = MemoryArticleRepository()
        self.fallback1 = MemoryArticleRepository()
        self.fallback2 = MemoryArticleRepository()

        return CombinedArticleRepository(
            primary_repository=self.primary,
            fallback_repositories=[
                self.fallback1,
                self.fallback2,
            ]
        )

    def test_load_fallback(self):
        """
        This code checks that we are able to load a article from the list of test fixtures.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"articles/test_fixtures/test_article_1.json").decode("utf-8")
        article = Article.from_json(data_str)
        article.id = "new_test_id"

        # Check that we can't load the article initially
        loaded_article = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_article)

        # Save the article into the fallback repository.
        self.fallback1.save(article)

        # Now try to load it from the combined repository.
        loaded_article = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(article)
        self.assertEqual(loaded_article, article)

    def test_load_second_fallback(self):
        """
        This code checks that if you have multiple fallbacks, you can still load data from the second fallbacks.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"articles/test_fixtures/test_article_1.json").decode("utf-8")
        article = Article.from_json(data_str)
        article.id = "new_test_id"

        # Check that we can't load the article initially
        loaded_article = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_article)

        # Save the article into the second fallback repository.
        self.fallback2.save(article)

        # Now try to load it from the combined repository.
        loaded_article = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(article)
        self.assertEqual(loaded_article, article)
