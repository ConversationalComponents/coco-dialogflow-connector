from flask import Flask, request, jsonify
from requests import HTTPError
import time

from DialogFlowManager import processor
from DialogFlowManager.custom_exceptions import DialogFlowLoadComponentError

import response_handler

from config import ACTIONS_MAPPING_CONFIG

# Init app.
app = Flask(__name__)

# Load configs.
app.config.update(ACTIONS_MAPPING_CONFIG)

# Error handlers.
@app.errorhandler(DialogFlowLoadComponentError)
def handle_component_not_exists(err):
    return jsonify({"error": f"Component was not found. ERROR: {str(err)}"}),\
           400, {}


@app.errorhandler(HTTPError)
def handle_bad_http_request(err):
    return jsonify({"error": f"HTTP error occurred. ERROR: {str(err)}"}),\
           400, {}

# Endpoints.
@app.route("/api/exchange/<component_id>/<session_id>", methods=["POST"])
def exchange(component_id, session_id):
    request_json = request.get_json() or {}

    user_input = request_json.get("user_input", " ")

    start_time = time.time()
    response = processor.process_request(component_id=component_id,
                                         session_id=session_id,
                                         text=user_input)
    end_time = time.time()

    res_time_seconds = end_time - start_time

    coco_standard_response = response_handler.handle(component_id, response,
                                                     response_time_seconds=res_time_seconds)

    return jsonify(coco_standard_response), 200, {}


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)




