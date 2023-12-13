from flask import make_response
from flask_restful import Resource, request
from dependency_injector.wiring import inject, Provide
from tussle.completions.providers.completion_provider_base import CompletionProviderBase
import json


class Completion(Resource):
    def __init__(self):
        super().__init__()

    @inject
    def post(self, completion_provider: CompletionProviderBase=Provide['completion_provider']):
        # Get the prompt from json
        prompt = request.get_json()['prompt']

        # Get the completion
        completion = completion_provider.get_completion(prompt, temperature=0.5)

        # Return the completion
        return make_response(json.dumps({
            'completion': completion
        }))
