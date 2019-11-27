import dialogflow_v2 as dialogflow
import logging
import json
import os

from .custom_exceptions import DialogFlowLoadComponentError

COMPONENTS_FOLDER_NAME = "components"


def _build_service_account_config_path(component_id):
    """
    Build service account json file full path.

    Arguments:
        component_id (string): Target DialogFlow component ID the name of
        the DialogFlow service account file without the extension.

    Returns:
        Service account config file path. (string)
    """
    components_folder_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), COMPONENTS_FOLDER_NAME)
    return f"{components_folder_name}/{component_id}.json"


def _load_service_account_config(component_id):
    """
    Fetch service account json content.

    Arguments:
        component_id (string): Target DialogFlow component ID the name of
        the DialogFlow service account file without the extension.

    Returns:
        Dialog service account config file json content. (dict)
    """

    config_file_path = _build_service_account_config_path(component_id)

    if not os.path.isfile(config_file_path):
        error_message = f"Component with ID: {component_id} does not exist."
        logging.error(error_message)
        raise DialogFlowLoadComponentError(error_message)

    with open(config_file_path, "r") as f:
        return json.loads(f.read())


def _create_session(component_id):
    """
    Initialize DialogFlow session client.

    Arguments:
        component_id (string): Target DialogFlow component ID the name of
        the DialogFlow service account file without the extension.

    Returns:
        DialogFlow Session Client. (DialogFlow Session Client)
    """
    config_file_path = _build_service_account_config_path(component_id)

    return dialogflow.SessionsClient.from_service_account_json(
        config_file_path)


def process_request(component_id, session_id, text, language_code="en"):
    """
    Returns bot output for user input.

    Using the same `session_id` between requests allows continuation
    of the conversation.

    Arguments:
        component_id (string): Target DialogFlow component ID the name of
        the DialogFlow service account file without the extension.
        session_id (string): Current session ID.
        text (string): User input.
        language_code (string): Context language.
    Returns:
        DialogFlow response object. (DialogFlow Response)
    """
    service_account_config = _load_service_account_config(component_id)
    component_session_client = _create_session(component_id)

    project_id = service_account_config.get("project_id")

    session = component_session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text,
                                            language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = component_session_client.detect_intent(session=session,
                                                      query_input=query_input)

    return response
