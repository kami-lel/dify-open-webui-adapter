"""
Integrate Open WebUI and Dify by exposing a Dify App
(Workflow or Chatflow) as Open WebUI model using Open WebUI's Pipe Functions.

Supported Open WebUI Version:   v0.6.30
Supported Dify Version:         1.10.0

User must configure these 2 constant in Python script before use:

``DIFY_BACKEND_API_BASE_URL``: base URL to access Dify Backend Service API

``APP_MODEL_CONFIGS``: a ``list`` of model/app config (each as ``dict``)

example for a single model/app::

    {
        "type": DifyAppType.WORKFLOW,  # Dify App Type
        "key": "...",             # Backend Service API secret key of Dify App
        "model_id": "model_id1",  # model id as used in Open WebUI
        "name": "First Model",    # model Name as appeared in Open WebUI, optional
    }

example for ``APP_MODEL_CONFIGS``::

    APP_MODEL_CONFIGS = [
        {
            "type": DifyAppType.WORKFLOW,
            "key": "...",
            "model_id": "model_id1",
        },
        {
            ~  # config for 2nd app/model
        },
    ]
"""

# Todo implement stream mode

from enum import Enum
import json

from pydantic import BaseModel
import requests

# adapter version
__version__ = "2.0.1-alpha"
__author__ = "kamiLeL"


class DifyAppType(Enum):
    """
    type of Dify App, either Workflow or Chatflow (multi-round)
    """

    WORKFLOW = 0
    CHATFLOW = 1  # multi-turn chats


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"

APP_MODEL_CONFIGS = []


# constant  ####################################################################
OWU_USER_ROLE = DIFY_USER_ROLE = "user"
REQUEST_TIMEOUT = 30


# data & logic Container  ######################################################
def verify_app_model_configs(app_model_configs):
    """
    verify users' settings of APP_MODEL_CONFIGS

    :raises ValueError: APP_MODEL_CONFIGS is invalid
    """
    if len(app_model_configs) == 0:
        raise ValueError(
            "APP_MODEL_CONFIGS must contains at least one App/Model"
        )

    for config in app_model_configs:
        # test type  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "type" not in config:
            raise ValueError("APP_MODEL_CONFIGS missing 'type' entry")
        if not isinstance(config["type"], DifyAppType):
            raise TypeError(
                "APP_MODEL_CONFIGS 'type' entry must be DifyAppType"
            )
        # test key  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "key" not in config:
            raise ValueError("APP_MODEL_CONFIGS missing 'key' entry")
        if not isinstance(config["key"], str):
            raise TypeError("APP_MODEL_CONFIGS 'key' entry must be str")
        if len(config["key"]) == 0:
            raise ValueError("APP_MODEL_CONFIGS 'key' must not be empty")
        # test id  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "model_id" not in config:
            raise ValueError("APP_MODEL_CONFIGS missing 'model_id' entry")
        if not isinstance(config["model_id"], str):
            raise TypeError("APP_MODEL_CONFIGS 'model_id' entry must be str")
        if len(config["model_id"]) == 0:
            raise ValueError("APP_MODEL_CONFIGS 'model_id' must not be empty")
        # test name  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "name" in config:
            name = config["name"]
            if isinstance(name, str):
                if len(name) == 0:
                    raise ValueError(
                        "APP_MODEL_CONFIGS 'name' must not be empty"
                    )
            elif name is not None:
                raise TypeError(
                    "APP_MODEL_CONFIGS 'name' entry must be str or None"
                )


def create_container(base_url, app_model_config):
    """
    create an instance of specific sub-types of BaseContainer


    :param base_url:
    :type base_url: str
    :param config: an entry of APP_MODEL_CONFIGS
    :type config: dict
    :return: created container
    :rtype: WorkflowContainer or ChatflowContainer
    """
    model_type = app_model_config["type"]
    key = app_model_config["key"]
    model_id = app_model_config["model_id"]
    name = None  # default
    if "name" in app_model_config:
        model_name_value = app_model_config["name"]
        if isinstance(model_name_value, str):
            name = model_name_value

    if model_type == DifyAppType.WORKFLOW:
        return WorkflowContainer(base_url, key, model_id, name)
    else:  # i.e. Chatflow
        raise TypeError("Chatflow not implemented in this version")
        # Todo
        # return ChatflowContainer(base_url, key, model_id, name)


class BaseContainer:
    """
    base class for WorkflowContainer and ChatflowContainer


    :param base_url:
    :type base_url: str
    :param key:
    :type key: str
    :param model_id:
    :type model_id: str
    :param name:
    :type name: str or NoneType
    """

    def __init__(self, base_url, key, model_id, name):
        # Todo validate key
        self.base_url = base_url
        self.key = key
        self.model_id = model_id
        self._name = name  # may be None

    def get_model_id_and_name(self):
        """
        :return: an entry of this model,
                such that it can be served to ``Pipe.pipes()``
        :rtype: dict{str: str}
        """
        return {"id": self.model_id, "name": self.name}

    def reply(self, body, user):
        """
        main logic for fetching & creating a single-round response


        :param body: `body` given by OWU Pipe.pipes(body, __user__)
        :type body: dict
        :param user: `__user__` given by Pipe.pipes(body, __user__)
        :type user: dict
        :raises ConnectionError: fail Dify request
        :return: the response
        :rtype: str
        """
        # extract from OWU  ++++++++++++++++++++++++++++++++++++++++++++++++++++
        newest_user_message = self._retrieve_newest_user_message(body)
        url = self._gen_request_url()
        html_headers = self._gen_html_header()
        payload = json.dumps(self._build_html_payloads(newest_user_message))

        # POST Dify  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        try:
            html_response = requests.post(
                url,
                headers=html_headers,
                data=payload,
                timeout=REQUEST_TIMEOUT,
            )
            html_response.raise_for_status()

        # handle network errors
        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail Dify request: {}".format(err.args[0])
            ) from err

        # extract response  ++++++++++++++++++++++++++++++++++++++++++++++++++++
        response_json = html_response.json()
        return self._extract_dify_response(response_json)

    @property
    def name(self):
        """
        :return: display name of this app/model; model id if no name is given
        :rtype: str
        """
        return self._name or self.model_id

    def _retrieve_newest_user_message(self, body):
        """
        :param body: `body` given by OWU Pipe.pipes(body, __user__)
        :type body: dict
        :raises KeyError: `body` is malformed
        :raises ValueError: no `user` message in `body
        :return: retrieved newest user's message
        :rtype: str
        """

        for msg in reversed(body["messages"]):
            if msg["role"] == OWU_USER_ROLE:
                return msg["content"]

        raise ValueError("fail to find any 'user' messages")

    def _gen_request_url(self):
        """
        :return: url to access Dify Backend API
        :rtype: str
        """
        raise NotImplementedError

    def _gen_html_header(self):
        """
        :return: header (including authorization info) sent to Dify Backend API
        :rtype: dict
        """
        return {
            "Authorization": "Bearer {}".format(self.key),
            "Content-Type": "application/json",
        }

    def _build_html_payloads(self, newest_user_message):
        """
        :return: payload data sent to Dify Backend API
        :rtype: dict
        """
        raise NotImplementedError

    def _extract_dify_response(self, response_json):
        """
        extract bot's response message out of response from Dify


        :param response_json:
        :type response_json:
        :return: per-round message content extracted from Dify's response
        :rtype: str
        """
        raise NotImplementedError

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.name)


class WorkflowContainer(BaseContainer):
    """
    data & logic container for handling Dify Workflow App
    """

    def _gen_request_url(self):
        return "{}/workflows/run".format(self.base_url)

    def _build_html_payloads(self, newest_user_message):
        inputs = {"input": newest_user_message}

        payload_dict = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": DIFY_USER_ROLE,
        }

        return payload_dict

    def _extract_dify_response(self, response_json):
        """
        :raises KeyError: malformed `response_json`
        """
        try:
            return response_json["data"]["outputs"]["output"]
        except KeyError as err:
            raise KeyError(
                "fail to parse Dify response, missing key: {}".format(
                    err.args[0]
                )
            ) from err


class ChatflowContainer(BaseContainer):
    """
    data & logic container for handling Dify Chatflow App (multi-round)
    """

    def _gen_request_url(self):
        # Bug need test
        return "{}/chat-messages".format(self.base_url)

    def _build_html_payloads(self, newest_user_message):
        # def _build_payload_chatflow(
        #     self, message, conversation_id, everything_for_debug
        # ):
        #     inputs = {}
        #     if ENABLE_DEBUG:
        #         inputs["everything_for_debug"] = everything_for_debug

        #     return {
        #         "inputs": inputs,
        #         "query": message,
        #         "response_mode": "blocking",
        #         "conversation_id": conversation_id,
        #         "user": USER_ROLE,
        #         "auto_generate_name": False,
        #     }
        raise NotImplementedError  # Hack

    def _extract_dify_response(self, response_json):
        # def _extract_output_chatflow(
        #     self, model_id, response_json, saved_conversation_id
        # ):
        #     try:
        #         output = response_json["answer"]

        #         # save returned conversation idea for future rounds
        #         if not saved_conversation_id:
        #             conversation_id = response_json["conversation_id"]
        #             self.model_data[model_id][2] = conversation_id

        #             if ENABLE_DEBUG:
        #                 conversation_id = response_json["conversation_id"]
        #                 self.model_data[model_id][2] = conversation_id
        #                 self.debug_lines.append("## returned conversation id")
        #                 self.debug_lines.append(conversation_id)

        #     except (KeyError, IndexError) as err:
        #         raise ValueError(
        #             "fail to parse chatflow response {}: {}".format(
        #                 response_json, err
        #             )
        #         ) from err

        #     return output
        raise NotImplementedError  # Hack


# Pipe class required by OWU  ##################################################
class Pipe:  # pylint: disable=missing-class-docstring

    class Valves(BaseModel):
        pass  # configuration via Python constants

    def __init__(
        self, app_model_configs_override=None, base_url_override=None
    ):
        base_url = base_url_override or DIFY_BACKEND_API_BASE_URL

        app_model_configs = app_model_configs_override or APP_MODEL_CONFIGS
        verify_app_model_configs(app_model_configs)

        # populate containers   ++++++++++++++++++++++++++++++++++++++++++++++++
        self.containers = {}
        for config in app_model_configs:
            container = create_container(base_url, config)
            model_id = container.model_id
            self.containers[model_id] = container

    def pipes(self):
        """
        :return: all models, e.g.::

            [
                {"id": "model_id_1", "name": "First Model"},
                {"id": "model_id_2", "name": "Second Model"},
                {"id": "model_id_3", "name": "Third Model"},
            ]

        :rtype: list(dict)
        """
        return [
            container.get_model_id_and_name()
            for container in self.containers.values()
        ]

    def pipe(self, body, __user__):
        """
        main pipe logic per round


        :param body: message body
        :type body: dict
        :param __user__: user information
        :type __user__: dict
        :raises KeyError: missing `"model"` in `body`
        :return: replied message by the model
        :rtype: str
        """
        if "model" not in body:
            raise IndexError("missing entry 'model' in body")

        # extract model_id from body
        model_id = body["model"][body["model"].find(".") + 1 :]
        return self.containers[model_id].reply(body, __user__)
