from tussle.articles.data_repository.memory.memory_article_repository import MemoryArticleRepository
from tussle.articles.components.article import Article
from tussle.articles.data_repository.article_repository_base import ArticleRepositoryBase
import pkg_resources


class CombinedArticleRepository(ArticleRepositoryBase):
    """
    This is a data repository that combines together other data repositories.
    It has a main repository which is where data is saved and loaded from.
    But it has a secondary function where it will load things from the
    fallback repositories if it can.
    """

    def __init__(self, primary_repository: ArticleRepositoryBase, fallback_repositories: list[ArticleRepositoryBase]):
        self.primary_repository = primary_repository
        self.fallback_repositories = fallback_repositories

    def get_by_id(self, article_id: str):
        """
        Gets a article by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the primary repository.
        article = self.primary_repository.get_by_id(article_id)
        if article:
            return article

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            article = fallback_repository.get_by_id(article_id)
            if article:
                # Save it into the primary repository
                self.primary_repository.save(article)
                return article

        return None

    def get_by_slug(self, slug: str) -> (Article | None):
        """
        Gets an article by its slug.
        """
        # First attempt to get it from the primary repository.
        article = self.primary_repository.get_by_slug(slug)
        if article:
            return article

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            article = fallback_repository.get_by_slug(slug)
            if article:
                # Save it into the primary repository
                self.primary_repository.save(article)
                return article

        return None

    def create(self, article: Article):
        """
        Creates a brand new article object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The article object with the 'id' field assigned.
        """
        return self.primary_repository.create(article)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the articles created for the given owner.
        """
        return self.primary_repository.get_all_by_owner(owner)

    def get_all(self):
        """
        Fetches all the articles created for the given owner.
        """
        return self.primary_repository.get_all()

    def get_all_published(self):
        """
        Fetches all the published articles found in the system.
        """
        return self.primary_repository.get_all_published()

    def delete_by_id(self, article_id: str):
        """
        Deletes a article by its ID.
        """
        return self.primary_repository.delete_by_id(article_id)

    def save(self, article: Article):
        """
        Saves the given article.
        """
        return self.primary_repository.save(article)

    def delete_all(self):
        """
        Deletes all the articles.
        """
        return self.primary_repository.delete_all()
