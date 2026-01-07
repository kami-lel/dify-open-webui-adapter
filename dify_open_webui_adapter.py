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

Q.v. ``https://github.com/kami-lel/dify-open-webui-adapter``
"""

# adapter version
__version__ = "2.0.1-alpha"
__author__ = "kamiLeL"


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"

APP_MODEL_CONFIGS = []


# end of config  ###############################################################

# pylint: disable=wrong-import-position
from enum import Enum
import json

from pydantic import BaseModel
import requests

# constants  ###################################################################
OWU_USER_ROLE = DIFY_USER_ROLE = "user"
DIFY_INPUT_VARIABLE_NAME = "input"
DIFY_OUTPUT_VARIABLE_NAME = "output"
REQUEST_TIMEOUT = 30


# helper Enum  #################################################################
class DifyAppType(Enum):
    """
    type of Dify App, either Workflow or Chatflow (multi-round)
    """

    # value of enums are identical to them appearing
    # in Dify Backend API's /info response
    WORKFLOW = "workflow"
    CHATFLOW = "advanced-chat"  # multi-turn chats


# OpenWeb UI model container  ##################################################
class OWUModel:
    """
    logic & data container representing a single pipe **model** in Open WebUI,
    handling OWU side's logic (parse `body`, etc.)


    :param base_url:
    :type base_url: str
    :param config: an entry of APP_MODEL_CONFIGS
    :type config: dict
    :raises ValueError:
    :raises TypeError:
    """

    def __init__(
        self,
        base_url,
        app_model_config,
        *,
        disable_get_app_type_and_name_by_dify_get_info=False,
        app_type_override=None,
    ):
        self.base_url = base_url

        self.key, self.model_id, provided_name = (
            self._parse_app_model_config_arg(app_model_config)
        )

        app_type, response_name = self._get_app_type_and_name_by_dify_get_info(
            disable=disable_get_app_type_and_name_by_dify_get_info
        )
        if app_type_override is not None:  # for unit test w/o network
            app_type = app_type_override

        # set self.name
        self.name = provided_name or response_name or self.model_id

        # create app
        if app_type == DifyAppType.WORKFLOW:
            self.app = WorkflowDifyApp(self)
        else:
            self.app = ChatflowDifyApp(self)

    def get_model_id_and_name(self):
        """
        :return: an entry of this model,
                such that it can be served to ``Pipe.pipes()``
        :rtype: dict{str: str}
        """
        return {"id": self.model_id, "name": self.name}

    def reply(self, body, user):
        """
        handle OWU side of processing per-round response of conversation


        :param body: `body` given by OWU Pipe.pipes(body, __user__)
        :type body: dict
        :param user: `__user__` given by Pipe.pipes(body, __user__)
        :raises ValueError:
        :raises ConnectionError:
        :return: the response
        :rtype: str
        """

        # extract info from OWU's body  ----------------------------------------
        newest_msg = self._get_newest_user_message_from_body(body)

        # extract if stream is enabled
        try:
            enable_stream = bool(body["stream"])
        except KeyError as err:
            raise ValueError() from err

        # call DifyApp  --------------------------------------------------------
        opt = self.app.reply(newest_msg, enable_stream)

        return opt

    def http_header(self, enable_stream=False):
        """
        :return: HTTP header (including authorization info)
                to access Dify Backend API
        :rtype: dict
        """
        header_dict = {
            "Authorization": "Bearer {}".format(self.key),
            "Content-Type": (
                "text/event-stream" if enable_stream else "application/json"
            ),
        }

        return header_dict

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

    def _get_app_type_and_name_by_dify_get_info(self, disable=False):
        """
        by GET /info endpoint of Dify Backend API,
        get Dify app type and its name

        helper method used in __init__()


        :raises ConnectionError:
        :raises ValueError:
        :return: App name & type responded from Dify
        :rtype: tuple(str, DifyAppType)
        """
        if disable:  # disable network-related function for unit tests
            return None, None

        info_url = "{}/info".format(self.base_url)

        # GET /info  -----------------------------------------------------------
        try:
            response_object = requests.get(
                info_url,
                headers=self.http_header(),
                timeout=REQUEST_TIMEOUT,
            )
            response_object.raise_for_status()
            response = response_object.json()

        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail Dify request: {}".format(err.args[0])
            ) from err

        # parse App type  ------------------------------------------------------
        try:
            app_type = DifyAppType(response["mode"])
        except (KeyError, ValueError) as err:
            raise ValueError(
                "fail to get App type from Dify: {}".format(err.args[0])
            ) from err

        response_name = response["name"] if "name" in response else None

        return app_type, response_name

    def _get_newest_user_message_from_body(self, body):
        for section in reversed(body["messages"]):
            if section["role"] == OWU_USER_ROLE:
                return section["content"]

        raise ValueError(
            "fail to find any '{}' messages".format(OWU_USER_ROLE)
        )

    def __repr__(self):
        return "OWUModel({}:{})".format(self.name, repr(self.app))


# Dify App container  ##########################################################
class BaseDifyApp:
    """
    logic container representing an **App** in Dify,
    handling Dify Backend API side's logic
    (create payload satisfying Dify's syntax, etc.)


    :param model:
    :type model: OWUModel
    """

    def __init__(self, model):
        self.model = model

    # pylint: disable=missing-function-docstring
    @property
    def base_url(self):
        return self.model.base_url

    @property
    def model_id(self):
        return self.model.model_id

    @property
    def name(self):
        return self.model.name

    @property
    def endpoint_url(self):
        """
        :return: endpoint URL to access Dify
        :rtype: str
        """
        raise NotImplementedError

    def http_header(self, enable_stream=False):
        return self.model.http_header(enable_stream=enable_stream)

        # pylint: enable=missing-function-docstring

    def reply(self, newest_msg, enable_stream):
        """
        handle Dify side of processing per-round response of conversation,
        by requesting Dify Backend API


        :raises ConnectionError: fail Dify request
        """
        raise NotImplementedError

    def build_request_payload(self, newest_msg, enable_stream):
        """
        :param newest_msg:
        :type newest_msg: str
        :param enable_stream:
        :type enable_stream: bool
        :return:
        :rtype: dict
        """
        raise NotImplementedError

    def _create_requests_response_json(self, newest_msg):
        """
        :param newest_msg:
        :type newest_msg: str
        :return: a response object's json
        :rtype: dict
        """
        try:
            response_object = requests.post(
                self.endpoint_url,
                headers=self.http_header(),
                data=json.dumps(self.build_request_payload(newest_msg, False)),
                stream=False,
                timeout=REQUEST_TIMEOUT,
            )
            response_object.raise_for_status()
            return response_object.json()

        # handle network errors
        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail Dify request: {}".format(err.args[0])
            ) from err

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.name)


class WorkflowDifyApp(BaseDifyApp):
    """
    representing a Workflow App in Dify
    """

    @property
    def endpoint_url(self):
        return "{}/workflows/run".format(self.base_url)

    def reply(self, newest_msg, enable_stream):
        # FIXME not implementing streaming
        return self._reply_blocking(newest_msg)

    def build_request_payload(self, newest_msg, enable_stream):
        payload_dict = {
            "inputs": {DIFY_INPUT_VARIABLE_NAME: newest_msg},
            "response_mode": "streaming" if enable_stream else "blocking",
            "user": DIFY_USER_ROLE,
        }
        return json.dumps(payload_dict)

    def _reply_blocking(self, newest_msg):
        # Todo refactor to be simplified
        try:
            response_object = requests.post(
                self.endpoint_url,
                headers=self.http_header(),
                data=self.build_request_payload(newest_msg, False),
                timeout=REQUEST_TIMEOUT,
            )
            response_object.raise_for_status()

        # handle network errors
        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail Dify request: {}".format(err.args[0])
            ) from err

        # parse response  ------------------------------------------------------
        response = response_object.json()
        try:
            return response["data"]["outputs"][DIFY_OUTPUT_VARIABLE_NAME]
        except KeyError as err:
            raise KeyError(
                "fail to parse Dify response, missing key: {}".format(
                    err.args[0]
                )
            ) from err


class ChatflowDifyApp(BaseDifyApp):
    """
    representing a Chatflow App in Dify
    """

    class _ChatMessageTask:
        """
        HACK fake streaming
        """

        def __init__(self, app, newest_msg):
            self._app = app
            self._newest_msg = newest_msg

            self._url = None

            # set up session  --------------------------------------------------
            self._session = requests.Session()
            self._session.headers = self._app.http_header()

            self._tmp_counter = 5

        def __iter__(self):
            return self

        def __next__(self):
            # HACk
            if self._tmp_counter == 0:
                self._session.close()
                raise StopIteration
            else:
                self._tmp_counter += 1

            if self._url is None:
                # 1st response, set up session
                self._url = self._app.endpoint_url
                response = self._session.post(
                    self._url,
                    data=json.dumps(
                        self._app.build_request_payload(self._newest_msg, True)
                    ),
                    stream=True,
                    timeout=None,
                )

            else:
                # 2nd & further requests
                response = self._session.post(self._url)

            # BUG way to handle
            try:
                return "{}\n\n----\n\n".format(next(response.iter_lines()))
            except StopIteration:
                pass
            finally:
                response.close()

    def __init__(self, model):
        super().__init__(model)
        self.conversation_id = ""

    @property
    def endpoint_url(self):
        return "{}/chat-messages".format(self.base_url)

    def reply(self, newest_msg, enable_stream):
        return (
            self._reply_streaming(newest_msg)
            if enable_stream
            else self._reply_blocking(newest_msg)
        )

    def build_request_payload(self, newest_msg, enable_stream):
        return {
            "query": newest_msg,
            "response_mode": "streaming" if enable_stream else "blocking",
            "user": DIFY_USER_ROLE,
            "conversation_id": self.conversation_id,
            "auto_generate_name": False,
            "inputs": {},
        }

    def _reply_streaming(self, newest_msg):
        return self._ChatMessageTask(self, newest_msg)

    def _reply_blocking(self, newest_msg):
        # parse response  ------------------------------------------------------
        response = self._create_requests_response_json(newest_msg)
        try:
            if not self.conversation_id:  # 1st round of this conversation
                self.conversation_id = response["conversation_id"]

            return response["answer"]

        except KeyError as err:
            raise ValueError(
                "fail to parse response body: {}".format(err.args[0])
            ) from err


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
            model.get_model_id_and_name()
            for model in self.model_containers.values()
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
        opt = self.model_containers[model_id].reply(body, __user__)

        return opt
