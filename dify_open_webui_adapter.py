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
#     "key": "...",             # Backend Service API secret key of Dify App
#     "model_id": "model_id1",  # model id as used in Open WebUI
#     "name": "First Model",    # model Name as appeared in Open WebUI, optional
# }
APP_MODEL_CONFIGS = []


# config  ######################################################################
USER_ROLE = "user"
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
        return ChatflowContainer(base_url, key, model_id, name)


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
        self.base_url = base_url
        self.key = key
        self.model_id = model_id
        self.name = name  # may be None

    def get_model_id_and_name(self):
        """
        :return: an entry of this model,
                such that it can be served to ``Pipe.pipes()``
        :rtype: dict{str: str}
        """
        display_name = self.name or self.model_id
        return {"id": self.model_id, "name": display_name}

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

        newest_user_message = self._retrieve_newest_user_message(body)
        return newest_user_message  # HACK

    def _retrieve_newest_user_message(self, body):
        try:
            for msg in body["messages"][-1]:
                if msg["role"] == USER_ROLE:
                    return msg["content"]

            # TODO change language
            raise ValueError("fail to find 'user' after exhausting 'messages'")

        except (KeyError, IndexError, ValueError) as err:
            raise ValueError("bad retrieve") from err  # TODO improve

    # self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL

    # self.debug_lines = []

    # # retrieve user input  -------------------------------------------------
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


count = 0  # HACK


class WorkflowContainer(BaseContainer):
    """
    data & logic container for handling Dify Workflow App
    """

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
    """
    data & logic container for handling Dify Chatflow App (multi-round)
    """

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

    def __init__(self, app_model_configs=APP_MODEL_CONFIGS):
        verify_app_model_configs(app_model_configs)
        self.containers = {}
        # populate containers   ++++++++++++++++++++++++++++++++++++++++++++++++
        base_url = self.Valves().DIFY_BACKEND_API_BASE_URL
        for config in APP_MODEL_CONFIGS:
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
        :return: replied message by the model
        :rtype: str
        """
        # extract model_id from body
        model_id = body["model"][body["model"].find(".") + 1 :]
        return self.containers[model_id].reply(body, __user__)
