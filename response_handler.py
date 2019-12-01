import copy

from config import ACTIONS_MAPPING_CONFIG

COCO_STANDARD_RESPONSE = {
    "action_name": "",
    "component_done": False,  # Bool
    "component_failed": False,  # Bool
    "confidence": 1,
    "out_of_context": False,  # Bool
    "response": "",
    "response_time": 0.0,
    "updated_context": {}
}


def handle(component_id, dialogflow_response, response_time_seconds=0.0):
    """
    Receives a DialogFlow result object and formats it to a standard CoCo
    component response format.

    Arguments:
        component_id (string): Target DialogFlow component ID the name of
        the DialogFlow service account file without the extension.
        dialogflow_response (Dialogflow Result Object):  Object returned from
        a Dialogflow SDK for detect_intent request.
        response_time_seconds (float): The time between the request and when
        the response was received.

    Returns:
        Result in a CoCo standard format. (dict)
    """
    mapping_config = ACTIONS_MAPPING_CONFIG[component_id]

    coco_standard_response = copy.deepcopy(COCO_STANDARD_RESPONSE)
    coco_standard_response["action_name"] = \
        dialogflow_response.query_result.intent.display_name
    coco_standard_response["response"] =\
        dialogflow_response.query_result.fulfillment_text
    coco_standard_response["response_time"] = response_time_seconds

    coco_standard_response["confidence"] = \
        dialogflow_response.query_result.intent_detection_confidence

    action_name = dialogflow_response.query_result.action

    coco_standard_response["component_done"] = \
        (mapping_config.get("COMPLETE_ACTION") == action_name)

    coco_standard_response["component_failed"] = \
        (mapping_config.get("FAILED_ACTION") == action_name)

    coco_standard_response["out_of_context"] = \
        (mapping_config.get("OUT_OF_CONTEXT_ACTION") == action_name)

    return coco_standard_response
