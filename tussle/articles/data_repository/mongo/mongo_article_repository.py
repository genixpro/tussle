from tussle.articles.data_repository.article_repository_base import ArticleRepositoryBase
from tussle.articles.components.article import Article
from tussle.general.db_models.custom_id_field import CustomIDField


class MongoArticleRepository(ArticleRepositoryBase):
    """
    This is a repository for articles which stores them in MongoDB.
    """
    def __init__(self, mongo_db_connection):
        self.mongo_db_connection = mongo_db_connection
        self.collection = self.mongo_db_connection['articles']
        self.create_indexes()

    def create_indexes(self):
        """
        This method is responsible for ensuring any indexes that are required
        to perform queries are created.
        """
        # Create an index on slug
        self.collection.create_index('slug', unique=True)

        # Create an index on published
        self.collection.create_index('published')

    def create(self, article: Article):
        """
        Creates a brand new article
        """
        if article.id is None:
            article.id = CustomIDField.generate_id("Article", article.owner)

        self.collection.insert_one(article.to_dict())

        return article


    def get_by_id(self, article_id: str):
        """
        Gets a bulk chart evaluation by its ID.
        """
        result = self.collection.find_one({'_id': article_id})
        if result is None:
            return None

        return Article.from_dict(result)

    def get_by_slug(self, slug: str) -> (Article | None):
        """
        Gets an article by its slug.
        """
        result = self.collection.find_one({'slug': slug})
        if result is None:
            return None

        return Article.from_dict(result)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the articles created for the given owner.
        """
        return [Article.from_dict(result) for result in self.collection.find({'owner': owner})]

    def get_all(self):
        """
        Fetches all the articles in the system.
        """
        return [Article.from_dict(result) for result in self.collection.find()]

    def get_all_published(self):
        """
        Fetches all the published articles found in the system.
        """
        return [Article.from_dict(result) for result in self.collection.find({'published': True})]

    def delete_by_id(self, article_id: str):
        """
        Deletes a bulk chart evaluation by its ID.
        """
        self.collection.delete_one({'_id': article_id})

    def save(self, article: Article):
        """
        Saves the given bulk chart evaluation json data.
        """
        self.collection.update_one({'_id': article.id}, {'$set': article.to_dict()})

    def delete_all(self):
        """
        Deletes all the bulk chart evaluations.
        """
        self.collection.delete_many({})


