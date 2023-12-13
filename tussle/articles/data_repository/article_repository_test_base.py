from tussle.articles.data_repository.article_repository_base import ArticleRepositoryBase
from tussle.articles.components.article import Article
from abc import ABCMeta, abstractmethod
import pkg_resources


class ArticleRepositoryTestBase(metaclass=ABCMeta):
    repository: ArticleRepositoryBase

    def setUp(self):
        self.repository = self.create_article_repository()

        # Delete anything in the repository in case there
        # is any data left over from previous tests.
        self.repository.delete_all()

    @abstractmethod
    def create_article_repository(self) -> ArticleRepositoryBase:
        """
        Creates a new file repository.
        """
        raise NotImplementedError('ArticleRepositoryTestBase.create_file_repository not implemented')

    def create_test_article(self):
        test_chart_data = pkg_resources.resource_string("tussle",
                                                        f"articles/test_fixtures/test_article_1.json").decode(
            "utf-8")
        chart = Article.from_json(test_chart_data)
        chart.owner = "test_owner"
        return chart

    def test_create(self):
        # Creates a file
        article = self.create_test_article()

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Checks to see that the new file has an ID
        self.assertIsNotNone(new_article._id)

        # Checks to see that the new file has the same owner
        self.assertEqual(new_article.owner, article.owner)

        # Check that the type is right
        self.assertIsInstance(new_article, Article)


    def test_get_by_id(self):
        # First create the file, then attempt to retrieve it back again
        article = self.create_test_article()

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Retrieves the file from the repository using the id
        retrieved_article = self.repository.get_by_id(new_article.id)

        # Checks to see that the retrieved file is the same object
        self.assertEqual(retrieved_article, new_article)

    def test_get_by_id_not_found(self):
        # Attempts to retrieve a file based on an id that doesn't exist
        retrieved_article = self.repository.get_by_id("non_existent_id")

        # Checks to see that the returned value is None
        self.assertIsNone(retrieved_article)

    def test_get_all_by_owner(self):
        # First create the file, then attempt to retrieve it back again
        article = self.create_test_article()

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Retrieves the file from the repository using the id
        retrieved_articles = self.repository.get_all_by_owner(new_article.owner)

        # Checks to see that the retrieved file is the same object
        self.assertEqual(len(retrieved_articles), 1)
        self.assertEqual(retrieved_articles[0], new_article)

    def test_get_all(self):
        # First create the file, then attempt to retrieve it back again
        article = self.create_test_article()

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Retrieves the file from the repository using the id
        retrieved_articles = self.repository.get_all()

        # Checks to see that the retrieved file is the same object
        self.assertEqual(len(retrieved_articles), 1)
        self.assertEqual(retrieved_articles[0], new_article)

    def test_delete_by_id(self):
        # First create the file, then attempt to retrieve it back again
        article = self.create_test_article()

        article.id = None

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Deletes the file from the repository
        self.repository.delete_by_id(new_article.id)

        # Attempts to retrieve the file from the repository using the id
        retrieved_article = self.repository.get_by_id(new_article.id)

        # Checks to see that the returned value is None
        self.assertIsNone(retrieved_article)

    def test_save(self):
        # First create the file, then attempt to retrieve it back again
        article = self.create_test_article()

        # Creates the file within the data repository
        new_article = self.repository.create(article)

        # Save the file
        self.repository.save(new_article)

        # Retrieves the file from the repository using the id
        retrieved_article = self.repository.get_by_id(new_article.id)

        # Checks to see that the retrieved file is the same object
        self.assertEqual(retrieved_article, new_article)
