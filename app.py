from flask import Flask, request, jsonify
from requests import HTTPError

from DialogFlowManager import processor
from DialogFlowManager.custom_exceptions import DialogFlowLoadComponentError

# Consts.


# Init app.
app = Flask(__name__)

# Error handlers.
@app.errorhandler(DialogFlowLoadComponentError)
def handle_bad_request(err):
    return jsonify({"error": f"Component was not found. ERROR: {str(err)}"}),\
           400, {}


@app.errorhandler(HTTPError)
def handle_bad_request(err):
    return jsonify({"error": f"HTTP error occurred. ERROR: {str(err)}"}),\
           400, {}

# Endpoints.
@app.route("/exchange/<component_id>/<session_id>", methods=["POST"])
def exchange(component_id, session_id):
    request_json = request.get_json() or {}

    response = processor.process_request(component_id=component_id,
                                         session_id=session_id,
                                         text=request_json.get("user_input"))

    return jsonify({"response": response.query_result.fulfillment_text}), 200, {}


if __name__ == "__main__":
    app.run(port=3000)




