from dependency_injector.wiring import inject, Provide
from flask import make_response
from flask_restful import Resource
from tussle.general.components.health_check.combined_concurrent_health_check import CombinedConcurrentHealthCheck
from tussle.general.logger import get_logger
from tussle.general.utils.hostname import get_host_name
import datetime
import json
import os


class HealthCheck(Resource):
    logger = get_logger("HealthCheck API")

    @inject
    def __init__(self ):
        self.health_check = CombinedConcurrentHealthCheck()

    def get(self):
        check_start_time = datetime.datetime.now()
        health_check_results = self.health_check.check()
        check_end_time = datetime.datetime.now()

        health_check_results['version'] = str(os.getenv("REVISION_ID"))
        health_check_results['host'] = get_host_name()
        health_check_results['check_start_time'] = check_start_time.isoformat()
        health_check_results['check_end_time'] = check_end_time.isoformat()

        result_json = json.dumps(health_check_results, indent=4)
        
        response = make_response(result_json)
        response.headers['Content-Type'] = 'application/json'

        if health_check_results['healthy']:
            response.status_code = 200
        else:
            response.status_code = 500

        return response
