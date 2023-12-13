from flask import Flask
from flask_cors import CORS
from tussle.general.apis.home_api import Home
from tussle.general.apis.health_check_api import HealthCheck
from tussle.completions.apis.completion_api import Completion
from tussle.articles.apis.article_api import ArticleGroup, ArticleSingle
from flask_restful import Api


def create_flask_app():
    """
        Create a Flask app with CORS enabled, and connects it to all APIs available in the
        system.
    """
    cache_config = {
        "CACHE_TYPE": "simple",
        "CACHE_DEFAULT_TIMEOUT": 300
    }

    flask_app = Flask(__name__)
    flask_app.config.from_mapping(cache_config)
    CORS(flask_app)
    api = Api(flask_app)

    api.add_resource(Home, '/')
    api.add_resource(HealthCheck, '/health_check')
    api.add_resource(Completion, '/completion')
    api.add_resource(ArticleGroup, '/article')
    api.add_resource(ArticleSingle, '/article/<string:article_id>')

    return flask_app

