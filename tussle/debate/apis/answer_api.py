from tussle.general.config.config import load_cloud_configuration
from cachetools import cached, TTLCache
from flask import request, Response, make_response
from flask_restful import Resource, reqparse, abort
from tussle.general.api_server.permissions import authenticate_user
from tussle.debate.components.answer import Answer
from dependency_injector.wiring import Provide, inject
import inspect


answer_cache = TTLCache(maxsize=128, ttl=300)
@inject
def lookup_answer_with_cache(answer_id, answer_repository=Provide['answer_repository']):
    """
    For users requesting answers while they aren't logged in, we will have a small local cache,
    just to improve performance if we get a rush of anonymous users all looking at the same answer.

    :param answer_id:
    :return:
    """
    if answer_id in answer_cache:
        return answer_cache[answer_id]

    answer = answer_repository.get_by_id(answer_id)
    if answer is None:
        answer = answer_repository.get_by_slug(answer_id)

    if answer is not None:
        answer_cache[answer_id] = answer
    return answer


def lookup_answer_and_check_access(perm):
    """
    This is a decorator that is used by the various answer endpoints / api_server to check permissions
    :param perm:
    :return:
    """
    def wrapper(api_func):
        allowed_args = [p for p in inspect.signature(api_func).parameters.keys() if p != 'self']

        @inject
        def wrapped(*args, answer_repository=Provide['answer_repository'], **kwargs):
            user = kwargs['user']
            answer_id = kwargs['answer_id']

            if not user:
                answer = lookup_answer_with_cache(answer_id)
            else:
                answer = answer_repository.get_by_id(answer_id)
                if answer is None:
                    answer = answer_repository.get_by_slug(answer_id)

            if answer is None:
                return abort(404)

            if not kwargs:
                kwargs = {}

            kwargs['answer'] = answer

            allowed = check_permissions_for_answer(answer, user, perm)

            if allowed:
                filtered_kwargs = {
                    k: v for k, v in kwargs.items() if k in allowed_args
                }

                return api_func(*args, **filtered_kwargs)
            else:
                return abort(403)

        return wrapped

    return wrapper


def check_permissions_for_answer(answer, user, perm):
    allowed = False
    if perm == "view":
        allowed = True
    elif perm == "edit":
        if answer.owner == user:
            allowed = True
    return allowed


class AnswerGroup(Resource):
    @inject
    def __init__(self, answer_repository=Provide['answer_repository']):
        self.postParser = reqparse.RequestParser()

        self.configData = load_cloud_configuration()

        self.answer_repository = answer_repository

    @authenticate_user(require_logged_in=False)
    def get(self, user):
        # Logged in users can see all answers in the system
        if user:
            answers = self.answer_repository.get_all()
        # Everyone else only sees the published answers.
        else:
            answers = self.answer_repository.get_all_published()

        response = make_response([answer.to_dict() for answer in answers])
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    def post(self, user):
        # Create a new answer
        answer = Answer(
            _id=None,
            owner=user,
            prompts=[],
        )

        self.answer_repository.create(answer)

        return answer.to_dict()


class AnswerSingle(Resource):
    @inject
    def __init__(self, answer_repository=Provide['answer_repository']):
        super().__init__()

        self.answer_repository = answer_repository

    @authenticate_user(require_logged_in=False)
    @lookup_answer_and_check_access("view")
    def get(self, answer):
        response = make_response(answer.to_dict())
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    @lookup_answer_and_check_access("edit")
    def delete(self, answer):
        del answer_cache[answer.id]
        self.answer_repository.delete_by_id(answer.id)

        return {}

    @authenticate_user(require_logged_in=True)
    @lookup_answer_and_check_access("edit")
    def put(self, answer):
        request_data = request.get_json()

        allowed_change_fields = [
            'topic_id',
            'answer',
        ]

        for field in allowed_change_fields:
            if field in request_data:
                setattr(answer, field, request_data[field])

        self.answer_repository.save(answer)

        # Update the local answer cache
        answer_cache[answer.id] = answer
