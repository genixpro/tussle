from flask import make_response
from flask_restful import Resource
import datetime
import json
import os
import socket


class Home(Resource):
    startTime = datetime.datetime.now()

    def get(self):
        version = os.getenv("REVISION_ID")

        response_data = {
            # This name field is checked for in cicd
            "name": "Tussle API Server",
            "version": str(version),
            "start_time": self.startTime.isoformat(),
            "current_time": datetime.datetime.now().isoformat(),
            "host": socket.gethostname()
        }

        response_json = json.dumps(response_data, indent=4)
        response = make_response(response_json)
        response.headers['Content-Type'] = 'application/json'
        return response
