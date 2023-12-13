from tussle.general.config.config import load_cloud_configuration
from cachetools import cached, TTLCache
from flask import request, Response, make_response
from flask_restful import Resource, reqparse, abort
from tussle.general.api_server.permissions import authenticate_user
from tussle.articles.components.article import Article, ArticlePrompt
from dependency_injector.wiring import Provide, inject
import inspect


article_cache = TTLCache(maxsize=128, ttl=300)
@inject
def lookup_article_with_cache(article_id, article_repository=Provide['article_repository']):
    """
    For users requesting articles while they aren't logged in, we will have a small local cache,
    just to improve performance if we get a rush of anonymous users all looking at the same article.

    :param article_id:
    :return:
    """
    if article_id in article_cache:
        return article_cache[article_id]

    article = article_repository.get_by_id(article_id)
    if article is None:
        article = article_repository.get_by_slug(article_id)

    if article is not None:
        article_cache[article_id] = article
    return article


def lookup_article_and_check_access(perm):
    """
    This is a decorator that is used by the various article endpoints / api_server to check permissions
    :param perm:
    :return:
    """
    def wrapper(api_func):
        allowed_args = [p for p in inspect.signature(api_func).parameters.keys() if p != 'self']

        @inject
        def wrapped(*args, article_repository=Provide['article_repository'], **kwargs):
            user = kwargs['user']
            article_id = kwargs['article_id']

            if not user:
                article = lookup_article_with_cache(article_id)
            else:
                article = article_repository.get_by_id(article_id)
                if article is None:
                    article = article_repository.get_by_slug(article_id)

            if article is None:
                return abort(404)

            if not kwargs:
                kwargs = {}

            kwargs['article'] = article

            allowed = check_permissions_for_article(article, user, perm)

            if allowed:
                filtered_kwargs = {
                    k: v for k, v in kwargs.items() if k in allowed_args
                }

                return api_func(*args, **filtered_kwargs)
            else:
                return abort(403)

        return wrapped

    return wrapper


def check_permissions_for_article(article, user, perm):
    allowed = False
    if perm == "view":
        allowed = True
    elif perm == "edit":
        if article.owner == user:
            allowed = True
    return allowed


class ArticleGroup(Resource):
    @inject
    def __init__(self, article_repository=Provide['article_repository']):
        self.postParser = reqparse.RequestParser()

        self.configData = load_cloud_configuration()

        self.article_repository = article_repository

    @authenticate_user(require_logged_in=False)
    def get(self, user):
        # Logged in users can see all articles in the system
        if user:
            articles = self.article_repository.get_all()
        # Everyone else only sees the published articles.
        else:
            articles = self.article_repository.get_all_published()

        response = make_response([article.to_dict() for article in articles])
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    def post(self, user):
        # Create a new article
        article = Article(
            _id=None,
            owner=user,
            prompts=[],
        )

        self.article_repository.create(article)

        return article.to_dict()


class ArticleSingle(Resource):
    @inject
    def __init__(self, article_repository=Provide['article_repository']):
        super().__init__()

        self.article_repository = article_repository

    @authenticate_user(require_logged_in=False)
    @lookup_article_and_check_access("view")
    def get(self, article):
        response = make_response(article.to_dict())
        response.add_etag()

        if request.if_none_match.contains(response.get_etag()[0]):
            response.status_code = 304
            response.data = ""
            return response

        return response

    @authenticate_user(require_logged_in=True)
    @lookup_article_and_check_access("edit")
    def delete(self, article):
        del article_cache[article.id]
        self.article_repository.delete_by_id(article.id)

        return {}

    @authenticate_user(require_logged_in=True)
    @lookup_article_and_check_access("edit")
    def put(self, article):
        request_data = request.get_json()

        if 'prompts' in request_data:
            article.prompts = [
                ArticlePrompt.from_dict(prompt) for prompt in request_data['prompts']
            ]

        allowed_change_fields = [
            'title',
            'slug',
            'question',
            'date',
            'paragraph_generating_prompt',
            'question_placeholder',
            'default_question_answer',
            'published',
        ]

        for field in allowed_change_fields:
            if field in request_data:
                setattr(article, field, request_data[field])

        self.article_repository.save(article)

        # Update the local article cache
        article_cache[article.id] = article
