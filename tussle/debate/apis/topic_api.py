from tussle.general.config.config import load_cloud_configuration
from cachetools import cached, TTLCache
from flask import request, Response, make_response
from flask_restful import Resource, reqparse, abort
from tussle.general.api_server.permissions import authenticate_user
from tussle.debate.components.topic import Topic
from dependency_injector.wiring import Provide, inject
import inspect


topic_cache = TTLCache(maxsize=128, ttl=300)
@inject
def lookup_topic_with_cache(topic_id, topic_repository=Provide['topic_repository']):
    """
    For users requesting topics while they aren't logged in, we will have a small local cache,
    just to improve performance if we get a rush of anonymous users all looking at the same topic.

    :param topic_id:
    :return:
    """
    if topic_id in topic_cache:
        return topic_cache[topic_id]

    topic = topic_repository.get_by_id(topic_id)
    if topic is None:
        topic = topic_repository.get_by_slug(topic_id)

    if topic is not None:
        topic_cache[topic_id] = topic
    return topic


def lookup_topic_and_check_access(perm):
    """
    This is a decorator that is used by the various topic endpoints / api_server to check permissions
    :param perm:
    :return:
    """
    def wrapper(api_func):
        allowed_args = [p for p in inspect.signature(api_func).parameters.keys() if p != 'self']

        @inject
        def wrapped(*args, topic_repository=Provide['topic_repository'], **kwargs):
            user = kwargs['user']
            topic_id = kwargs['topic_id']

            if not user:
                topic = lookup_topic_with_cache(topic_id)
            else:
                topic = topic_repository.get_by_id(topic_id)
                if topic is None:
                    topic = topic_repository.get_by_slug(topic_id)

            if topic is None:
                return abort(404)

            if not kwargs:
                kwargs = {}

            kwargs['topic'] = topic

            allowed = check_permissions_for_topic(topic, user, perm)

            if allowed:
                filtered_kwargs = {
                    k: v for k, v in kwargs.items() if k in allowed_args
                }

                return api_func(*args, **filtered_kwargs)
            else:
                return abort(403)

        return wrapped

    return wrapper


def check_permissions_for_topic(topic, user, perm):
    allowed = False
    if perm == "view":
        allowed = True
    elif perm == "edit":
        if topic.owner == user:
            allowed = True
    return allowed


class TopicGroup(Resource):
    @inject
    def __init__(self, topic_repository=Provide['topic_repository']):
        self.postParser = reqparse.RequestParser()

        self.configData = load_cloud_configuration()

        self.topic_repository = topic_repository

    @authenticate_user(require_logged_in=False)
    def get(self, user):
        # Logged in users can see all topics in the system
        if user:
            topics = self.topic_repository.get_all()
        # Everyone else only sees the published topics.
        else:
            topics = self.topic_repository.get_all_published()

        response = make_response([topic.to_dict() for topic in topics])
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    def post(self, user):
        # Create a new topic
        topic = Topic(
            _id=None,
            owner=user,
            prompts=[],
        )

        self.topic_repository.create(topic)

        return topic.to_dict()


class TopicSingle(Resource):
    @inject
    def __init__(self, topic_repository=Provide['topic_repository']):
        super().__init__()

        self.topic_repository = topic_repository

    @authenticate_user(require_logged_in=False)
    @lookup_topic_and_check_access("view")
    def get(self, topic):
        response = make_response(topic.to_dict())
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    @lookup_topic_and_check_access("edit")
    def delete(self, topic):
        del topic_cache[topic.id]
        self.topic_repository.delete_by_id(topic.id)

        return {}

    @authenticate_user(require_logged_in=True)
    @lookup_topic_and_check_access("edit")
    def put(self, topic):
        request_data = request.get_json()

        allowed_change_fields = [
            'description',
        ]

        for field in allowed_change_fields:
            if field in request_data:
                setattr(topic, field, request_data[field])

        self.topic_repository.save(topic)

        # Update the local topic cache
        topic_cache[topic.id] = topic
