from flask import Flask
from flask_cors import CORS
from tussle.general.apis.home_api import Home
from tussle.general.apis.health_check_api import HealthCheck
from tussle.completions.apis.completion_api import Completion
from tussle.debate.apis.topic_api import TopicGroup, TopicSingle
from tussle.debate.apis.answer_api import AnswerGroup, AnswerSingle
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
    api.add_resource(TopicGroup, '/topic')
    api.add_resource(TopicSingle, '/topic/<string:topic_id>')
    api.add_resource(AnswerGroup, '/answer')
    api.add_resource(AnswerSingle, '/answer/<string:answer_id>')

    return flask_app

