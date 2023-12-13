from tussle.articles.components.article import Article
import abc


class ArticleRepositoryBase(metaclass=abc.ABCMeta):
    """
    This is a base class for a data repository that stores articles.
    It acts as a go-between for the API and the database or another data layer.

    This class just defines the interface and doesn't actually implement anything.
    """

    def create(self, article: Article) -> Article:
        """
        Creates a brand new article object.

        This function should assign the 'id' field to the article.
        :return: The article object with the 'id' field assigned.
        """
        raise NotImplementedError('ArticleRepositoryBase.create not implemented')

    def get_by_id(self, article_id: str) -> (Article | None):
        """
        Gets a article by its ID.
        """
        raise NotImplementedError('ArticleRepositoryBase.get_by_id not implemented')

    def get_by_slug(self, slug: str) -> (Article | None):
        """
        Gets a article by its slug.
        """
        raise NotImplementedError('ArticleRepositoryBase.slug not implemented')

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the articles created for the given owner.
        """
        raise NotImplementedError('ArticleRepositoryBase.get_all_by_owner not implemented')

    def get_all(self):
        """
        Fetches all the articles in the system.
        """
        raise NotImplementedError('ArticleRepositoryBase.get_all not implemented')

    def get_all_published(self):
        """
        Fetches all the published articles found in the system.
        """
        raise NotImplementedError('ArticleRepositoryBase.get_all_published not implemented')

    def delete_by_id(self, article_id: str):
        """
        Deletes a article by its ID.
        """
        raise NotImplementedError('ArticleRepositoryBase.delete_by_id not implemented')

    def save(self, article: Article):
        """
        Saves the given article.
        """
        raise NotImplementedError('ArticleRepositoryBase.save not implemented')

    def delete_all(self):
        """
        Deletes all the articles.
        """
        raise NotImplementedError('ArticleRepositoryBase.save not implemented')


