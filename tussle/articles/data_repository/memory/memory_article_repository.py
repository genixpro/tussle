from tussle.articles.data_repository.article_repository_base import ArticleRepositoryBase
from tussle.articles.components.article import Article


class MemoryArticleRepository(ArticleRepositoryBase):
    """
    This is a simple repository for articles which just store them in memory.

    Chiefly useful for testing.
    """

    def __init__(self):
        self.id_counter = 0
        self.articles = {}

    def create(self, article: Article):
        """
        Creates a brand new article object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The article object with the 'id' field assigned.
        """
        if article.id is None:
            article.id = f"article-{self.id_counter}"
        self.id_counter += 1

        self.articles[article.id] = article
        return article

    def get_by_id(self, article_id: str):
        """
        Gets a article by its ID.
        """
        return self.articles.get(article_id)

    def get_by_slug(self, slug: str) -> (Article | None):
        """
        Gets an article by its slug.
        """
        for article in self.articles.values():
            if article.slug == slug:
                return article
        return None

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the articles created for the given owner.
        """
        return [article for article in self.articles.values() if article.owner == owner]

    def get_all(self):
        """
        Fetches all the articles in the system.
        """
        return [article for article in self.articles.values()]

    def get_all_published(self):
        """
        Fetches all the published articles found in the system.
        """
        return [article for article in self.articles.values() if article.published]

    def delete_by_id(self, article_id: str):
        """
        Deletes a article by its ID.
        """
        del self.articles[article_id]

    def save(self, article: Article):
        """
        Saves the given article.
        """
        self.articles[article.id] = article

    def delete_all(self):
        """
        Deletes all the articles.
        """
        self.articles = {}
