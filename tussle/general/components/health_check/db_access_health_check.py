from tussle.general.logger import get_logger
from tussle.general.db_models.custom_id_field import CustomIDField
from dependency_injector.wiring import inject, Provide
from .health_check_base import HealthCheckBase
from tussle.articles.data_repository.mongo.mongo_article_repository import MongoArticleRepository
import traceback
import random



class DbAccessHealthCheck(HealthCheckBase):
    """This verifies that connection to the db is online and that we can both create and delete a chart"""

    @inject
    def __init__(self, mongo_db_connection=Provide['mongo_db_connection']):
        super().__init__()
        self.logger = get_logger("DbAccessHealthCheck")
        self.mongo_db_connection = mongo_db_connection

    def check(self):
        try:
            # We try creating an entry in the health check table
            random_number = random.randint(0, 100000)

            self.mongo_db_connection['health_check'].insert_one({"random_number": random_number})

            results = list(self.mongo_db_connection['health_check'].find({"random_number": random_number}))
            result_count = len(results)

            self.mongo_db_connection['health_check'].delete_one({"random_number": random_number})

            self.logger.debug(f"DB access test result: Healthy: {result_count > 0}. Details: result_count: {result_count}")

            healthy = result_count > 0

            return {
                "healthy": healthy,
                "details": {
                    "result_count": result_count
                }
            }
        except Exception as e:
            self.logger.error(f"Error while checking db lookup:\n{traceback.format_exc()}")
            return {
                "healthy": False,
                "details": {
                    "error": traceback.format_exc()
                }
            }
