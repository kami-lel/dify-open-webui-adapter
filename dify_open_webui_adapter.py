"""
Integrate Open WebUI and Dify by exposing a Dify App
(Workflow or Chatflow) as Open WebUI model using Open WebUI's Pipe Functions.

Supported Open WebUI Version:   v???
Supported Dify Version:         ???
"""

from enum import Enum
import json

from pydantic import BaseModel, Field
import requests

# adapter version
__version__ = "1.1.1-alpha"
__author__ = "kamiLeL"


class DifyAppType(Enum):
    """
    type of Dify App, either Workflow or Chatflow (multi-round)
    """

    WORKFLOW = 0
    CHATFLOW = 1  # multi-turn chats


# app/model configs  ###########################################################
# app/model per entry:
# {
#     "type": DifyAppType.WORKFLOW,  # Dify App Type
#     "id": "model_id_1",       # model id as used in Open WebUI
#     "name": "First Model",    # model Name as appeared in Open WebUI, optional
# }
APP_MODEL_CONFIGS = []


# config  ######################################################################
ENABLE_DEBUGGING = False
USER_ROLE = "user"
REQUEST_TIMEOUT = 30


# data & logic Container  ######################################################


def verify_app_model_configs(app_model_configs):
    # FIXME maybe better way to do verification, w/ debug
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
        # test id  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "id" not in config:
            raise ValueError("APP_MODEL_CONFIGS missing 'id' entry")
        if not isinstance(config["id"], str):
            raise TypeError("APP_MODEL_CONFIGS 'id' entry must be str")
        if len(config["id"]) == 0:
            raise TypeError("APP_MODEL_CONFIGS 'id' must not be empty")
        # test name  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if "name" in config:
            if not isinstance(config["name"], str):
                raise TypeError("APP_MODEL_CONFIGS 'name' entry must be str")
            if len(config["name"]) == 0:
                raise TypeError("APP_MODEL_CONFIGS 'name' must not be empty")


def create_container(base_url, config):
    """
    create an instance of specific sub-types of BaseContainer


    :param base_url:
    :type base_url: str
    :param config: an entry of APP_MODEL_CONFIGS
    :type config: dict
    :return: created container
    :rtype: WorkflowContainer or ChatflowContainer
    """
    model_type = config["type"]
    model_id = config["id"]
    model_name = None  # default
    if "name" in config["name"]:
        model_name_value = config["name"]
        if isinstance(model_name_value, str):
            model_name = model_name_value

    if model_type == DifyAppType.WORKFLOW:
        return WorkflowContainer(base_url, model_id, model_name)
    else:  # i.e. Chatflow
        return ChatflowContainer(base_url, model_id, model_name)


class BaseContainer:
    """
    base class for WorkflowContainer and ChatflowContainer


    :param base_url:
    :type base_url: str
    :param model_id:
    :type model_id: str
    :param model_name:
    :type model_name: str or NoneType
    """

    def __init__(self, base_url, model_id, model_name):
        self.base_url = base_url
        self.model_id = model_id
        self.model_name = model_name  # may be None
        self._debug_lines = []

    def get_model_id_and_name(self):
        """
        :return: an entry of this model,
                such that it can be served to ``Pipe.pipes()``
        :rtype: dict{str: str}
        """
        display_name = self.model_name or self.model_id
        return {"id": self.model_id, "name": display_name}

    def _debug(self, line):
        """
        :param line:
        :type line: str
        """
        if not ENABLE_DEBUGGING:
            return

        self._debug_lines.append(line)

    def reply(self, body, user):
        """
        main logic for fetching & creating a single-round response


        :param body: `body` given by Pipe.pipes(body, __user__)
        :type body: dict
        :param user: `__user__` given by Pipe.pipes(body, __user__)
        :type user: dict
        :return: the response
        :rtype: str
        """

        # empty debug lines
        self._debug_lines = []

        raise NotImplementedError

        # return  # HACK
        # self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL

        # self.debug_lines = []

        # # retrieve user input  -------------------------------------------------
        # message = ""
        # try:
        #     for msg in body["messages"]:
        #         if msg["role"] == "user":
        #             message = msg["content"]
        #             break

        #     if not message:
        #         raise ValueError(
        #             "fail to find 'user' after exhausting 'messages'"
        #         )

        # except (KeyError, IndexError, ValueError) as err:
        #     raise ValueError(
        #         "fail to get user message from body {}: {}".format(body, err)
        #     ) from err

        # # Extract model id from the model name
        # model_id = body["model"][body["model"].find(".") + 1 :]
        # api_secret_key, app_type, conversation_id = self.model_data[model_id]

        # if ENABLE_DEBUG:
        #     self.debug_lines.append("## body")
        #     self.debug_lines.append(repr(body))
        #     self.debug_lines.append("## user message")
        #     self.debug_lines.append(message)
        #     self.debug_lines.append("## model id")
        #     self.debug_lines.append(model_id)
        #     self.debug_lines.append("## api secret key")
        #     self.debug_lines.append(api_secret_key)
        #     self.debug_lines.append("## conversation id")
        #     self.debug_lines.append(conversation_id)

        # # send request to Dify  ------------------------------------------------
        # url = self._gen_request_url(app_type)
        # headers = self._gen_headers(api_secret_key, app_type)
        # payloads = self._build_payload(
        #     message, app_type, conversation_id, everything_for_debug=body
        # )

        # try:
        #     response_json = requests.post(
        #         url,
        #         headers=headers,
        #         data=payloads,
        #         timeout=REQUEST_TIMEOUT,
        #     )
        # except Exception as err:
        #     raise ConnectionError(
        #         "fail to request POST:{}".format(err)
        #     ) from err

        # if ENABLE_DEBUG:
        #     self.debug_lines.append("## request url")
        #     self.debug_lines.append(url)
        #     self.debug_lines.append("## headers")
        #     self.debug_lines.append(str(headers))
        #     self.debug_lines.append("## payloads")
        #     self.debug_lines.append(str(payloads))

        # # output  --------------------------------------------------------------
        # response_json = response_json.json()

        # if ENABLE_DEBUG:
        #     self.debug_lines.append("## response content")
        #     self.debug_lines.append(repr(response_json))

        # output = self._extract_output(
        #     model_id, response_json, app_type, conversation_id
        # )

        # if ENABLE_DEBUG:
        #     self.debug_lines.append("\n\n----\n\n\n")
        #     self.debug_lines.append(output)

        # if ENABLE_DEBUG:
        #     return "\n".join(self.debug_lines)
        # else:
        #     return output

    # HACK cleanup
    # generate and build request  ##############################################

    # def _gen_request_url(self, app_type):
    #     if app_type == DifyAppType.WORKFLOW:
    #         return "{}/workflows/run".format(self.base_url)
    #     else:  # Chatflow
    #         return "{}/chat-messages".format(self.base_url)

    # def _gen_headers(self, api_secret_key, _):
    #     return {
    #         "Authorization": "Bearer {}".format(api_secret_key),
    #         "Content-Type": "application/json",
    #     }

    # def _build_payload(
    #     self, message, app_type, conversation_id, *, everything_for_debug
    # ):
    #     everything_for_debug = str(everything_for_debug)

    #     if app_type == DifyAppType.WORKFLOW:
    #         payload = self._build_payload_workflow(
    #             message, everything_for_debug
    #         )
    #     else:  # Chatflow
    #         payload = self._build_payload_chatflow(
    #             message, conversation_id, everything_for_debug
    #         )

    #     return json.dumps(payload)

    # def _extract_output(
    #     self, model_id, response_json, app_type, conversation_id
    # ):
    #     if app_type == DifyAppType.WORKFLOW:
    #         return self._extract_output_workflow(response_json)
    #     else:  # chatflow
    #         return self._extract_output_chatflow(
    #             model_id, response_json, conversation_id
    #         )


class WorkflowContainer(BaseContainer):

    def reply(self, body, user):
        return ""  # TODO

    # def _build_payload_workflow(self, message, everything_for_debug):
    #     inputs = {"input": message}
    #     if ENABLE_DEBUG:
    #         inputs["everything_for_debug"] = everything_for_debug

    #     payload_dict = {
    #         "inputs": inputs,
    #         "response_mode": "blocking",
    #         "user": USER_ROLE,
    #     }

    #     return payload_dict

    # def _extract_output_workflow(self, response_json):
    #     try:
    #         output = response_json["data"]["outputs"]["output"]
    #     except (KeyError, IndexError) as err:
    #         raise ValueError(
    #             "fail to parse response {}: {}".format(response_json, err)
    #         ) from err

    #     return output


class ChatflowContainer(BaseContainer):

    def reply(self, body, user):
        return ""  # Todo

    # Bug chatflow not working, only 1st message is repeated sent
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


# Pipe class required by OWU  ##################################################
class Pipe:  # pylint: disable=missing-class-docstring

    class Valves(BaseModel):
        DIFY_BACKEND_API_BASE_URL: str = Field(
            default="https://api.dify.ai/v1",
            description="base URL to access Dify Backend Service API",
        )

    def __init__(self):
        verify_app_model_configs(APP_MODEL_CONFIGS)
        self.containers = {}
        # populate app_models   ++++++++++++++++++++++++++++++++++++++++++++++++
        base_url = self.Valves().DIFY_BACKEND_API_BASE_URL
        for config in APP_MODEL_CONFIGS:
            container = create_container(base_url, config)
            model_name = container.model_id
            self.containers[model_name] = container

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
            container.get_model_id_and_name() for container in self.containers
        ]

    def pipe(self, body, __user__):
        """
        main pipe logic per round


        :param body: message body
        :type body: dict
        :param __user__: user information
        :type __user__: dict
        :return: replied message by the model
        :rtype: str
        """
        # extract model_id from body
        model_id = body["model"][body["model"].find(".") + 1 :]
        return self.containers[model_id].reply(body, __user__)
