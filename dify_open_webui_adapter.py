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
        "key": "...",             # Backend Service API secret key of Dify App
        "model_id": "model_id1",  # model id as used in Open WebUI
        "name": "First Model",    # model Name as appeared in Open WebUI
    }

example for ``APP_MODEL_CONFIGS``::

    APP_MODEL_CONFIGS = [
        {
            "key": "...",
            "model_id": "model_id1",
        },
        {
            ~  # config for 2nd app/model
        },
    ]
"""

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

    # value of enums are identical to them appearing
    # in Dify Backend API's /info response
    WORKFLOW = "workflow"
    CHATFLOW = "advanced-chat"  # multi-turn chats


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"

APP_MODEL_CONFIGS = []


# constant  ####################################################################
OWU_USER_ROLE = DIFY_USER_ROLE = "user"
REQUEST_TIMEOUT = 30


# OpenWeb UI model container  ##################################################
class OWUModel:
    """
    TODO docstring for class OWUModel


    :param base_url:
    :type base_url: str
    :param config: an entry of APP_MODEL_CONFIGS
    :type config: dict
    :raises ValueError:
    :raises TypeError:
    """

    def __init__(self, base_url, app_model_config):
        self.base_url = base_url

        self.key, self.model_id, provided_name = (
            self._parse_app_model_config_arg(app_model_config)
        )

        app_type, response_name = self._get_name_mode_by_dify_get_info()

        # set self.name
        self.name = provided_name or response_name or self.model_id

        # create app
        if app_type == DifyAppType.WORKFLOW:
            self.app = WorkflowDifyApp(self)
        else:
            self.app = ChatflowDifyApp(self)

    def _parse_app_model_config_arg(self, config):
        """
        test & parse ``app_model_config`` arg, then set:

        helper method used in __init__()


        :param config: app_model_config arg
        :type config: dict
        :raises ValueError:
        :raises TypeError:
        """
        # key  -----------------------------------------------------------------
        if "key" not in config:
            raise ValueError("entry in APP_MODEL_CONFIGS missing 'key'")
        key = config["key"]

        if not isinstance(key, str):
            raise TypeError("entry in APP_MODEL_CONFIGS must have str 'key'")

        if len(key) == 0:
            raise ValueError(
                "entry in APP_MODEL_CONFIGS must have non-empty 'key'"
            )

        # id  ------------------------------------------------------------------
        if "model_id" not in config:
            raise ValueError("entry in APP_MODEL_CONFIGS missing 'model_id'")
        model_id = config["model_id"]
        if not isinstance(model_id, str):
            raise TypeError(
                "entry in APP_MODEL_CONFIGS must have str 'model_id'"
            )
        if len(model_id) == 0:
            raise ValueError(
                "entry in APP_MODEL_CONFIGS must have non-empty 'model_id'"
            )

        # name  ----------------------------------------------------------------
        name = None
        if "name" in config:
            name = config["name"]
            if isinstance(name, str):
                if len(name) == 0:
                    raise ValueError(
                        "entry in APP_MODEL_CONFIGS must have non-empty 'name'"
                    )
            elif name is not None:
                raise TypeError(
                    "entry in APP_MODEL_CONFIGS, "
                    + "value of 'name' must be str or None"
                )

        return key, model_id, name

    def _get_name_mode_by_dify_get_info(self):
        """
        by GET /info endpoint of Dify Backend API,
        get Dify app type and its name

        helper method used in __init__()


        :raises ConnectionError:
        :raises ValueError:
        :return: App name & type responded from Dify
        :rtype: tuple(str, DifyAppType)
        """
        info_url = "{}/info".format(self.base_url)

        # GET /info  -----------------------------------------------------------
        try:
            response = requests.get(
                info_url,
                headers=self._create_html_authorization_header(),
                timeout=REQUEST_TIMEOUT,
            ).json()

        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail Dify request: {}".format(err.args[0])
            ) from err

        # parse name  ----------------------------------------------------------
        if "name" not in response:
            raise ValueError("")  # TODO
        response_name = response["name"]

        # parse App type  ------------------------------------------------------
        try:
            app_type = DifyAppType(response["mode"])
        except (KeyError, ValueError) as err:
            raise ValueError(
                "bad: {}".format(err.args[0])
            ) from err  # HACK better wording

        return response_name, app_type

    def _create_html_authorization_header(self):
        """
        :return: HTML header (including authorization info)
                to access Dify Backend API
        :rtype: dict
        """
        return {
            "Authorization": "Bearer {}".format(self.key),
            "Content-Type": "application/json",
        }


# Dify App container  ##########################################################
class BaseDifyApp:
    """
    TODO docstring for class BaseDifyApp
    """

    def __init__(self, model):
        self.model = model


class WorkflowDifyApp(BaseDifyApp):
    """
    TODO docstring for class WorkflowDifyApp
    """


class ChatflowDifyApp(BaseDifyApp):
    """
    TODO docstring for class ChatflowDifyApp
    """


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
        # TODO validate key
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
        # extract from OWU  ----------------------------------------------------
        newest_user_message = self._retrieve_newest_user_message(body)
        url = self._gen_request_url()
        html_headers = self._gen_html_header()
        payload = json.dumps(self._build_html_payloads(newest_user_message))

        # POST Dify  -----------------------------------------------------------
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

        # extract response  ----------------------------------------------------
        response_json = html_response.json()
        return self._extract_dify_response(response_json)

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


# helper methods  ##############################################################
def _check_app_model_configs_structure(app_model_configs):
    if len(app_model_configs) == 0:
        raise ValueError(
            "APP_MODEL_CONFIGS must contains at least one App/Model"
        )

    if any(not isinstance(config, dict) for config in app_model_configs):
        raise ValueError("APP_MODEL_CONFIGS must contains only dicts")


# Pipe class required by OWU  ##################################################
class Pipe:  # pylint: disable=missing-class-docstring

    class Valves(BaseModel):
        pass  # configuration via Python constants

    def __init__(
        self, app_model_configs_override=None, base_url_override=None
    ):
        base_url = base_url_override or DIFY_BACKEND_API_BASE_URL
        app_model_configs = app_model_configs_override or APP_MODEL_CONFIGS

        _check_app_model_configs_structure(app_model_configs)

        # populate containers   ------------------------------------------------
        self.model_containers = {}
        for config in app_model_configs:
            model = OWUModel(base_url, config)
            model_id = model.model_id
            self.model_containers[model_id] = model

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
            for container in self.model_containers.values()
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
        return self.model_containers[model_id].reply(body, __user__)
