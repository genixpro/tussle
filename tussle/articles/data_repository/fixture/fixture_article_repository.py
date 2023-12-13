from tussle.articles.data_repository.memory.memory_article_repository import MemoryArticleRepository
from tussle.articles.components.article import Article
import pkg_resources

class FixtureArticleRepository(MemoryArticleRepository):
    """
    This is a simple repository for bulk chart evaluations which just store them in memory.

    Chiefly useful for testing.
    """

    def get_by_id(self, article_id: str):
        """
        Gets a article by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the super class, the memory repository.
        article = super().get_by_id(article_id)
        if article:
            return article

        # Now attempt to load it from a fixture file.
        article = self._load_from_fixture(article_id)

        return article

    def _load_from_fixture(self, id):
        try:
            data_str = pkg_resources.resource_string("tussle", f"articles/test_fixtures/{id}.json").decode("utf-8")
        except FileNotFoundError:
            return None

            data_str = pkg_resources.resource_string("tussle", f"articles/test_fixtures/{id}.json").decode("utf-8")
        obj = Article.from_json(data_str)
        return obj
