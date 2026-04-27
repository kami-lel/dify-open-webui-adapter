"""
Integrating between: Open WebUI (abbr OWU) and Dify,
by exposing a Dify **app** (supporting Workflow and Chatflow)
as Open WebUI **model**.

Connecting with Dify app via *Dify Backend API*
and with OWU via *Pipe Function*.

Q.v. ``https://github.com/kami-lel/dify-open-webui-adapter``
"""

# adapter version
__version__ = "3.0.0-alpha"
__author__ = "kamiLeL"


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"
APP_MODEL_CONFIGS = []


# debug flags  =================================================================
DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE = False
DEBUG_PIPE_DIRECT_RESPONSE = False


# end of config  ###############################################################

# pylint: disable=wrong-import-position


from enum import Enum
import json
from typing import Optional
import requests

from pydantic import BaseModel, Field, computed_field


# helpers  #####################################################################
class AppModelConfig(BaseModel):  # ============================================
    """
    data structure to contain & validate configuration related to
    a single connection between Dify App and OWU Model

    i.e. a single entry in ``APP_MODEL_CONFIGS``
    """

    # fields  ******************************************************************

    # required
    key: str = Field(..., min_length=1)
    model_id: str = Field(..., min_length=1)

    # optional
    name: Optional[str] = Field(default=None, min_length=1)
    disallows_streaming: Optional[bool] = Field(default=False)

    # relevant only to Workflow
    query_input_field_identifier: Optional[str] = Field(
        default="query", min_length=1
    )
    reply_output_variable_identifier: Optional[str] = Field(
        default="answer", min_length=1
    )

    # todo pass thru variables

    # Public Methods ***********************************************************

    @staticmethod
    def validate_app_model_configs(app_model_configs):
        """
        validate basic structure of ``APP_MODEL_CONFIGS``


        :param app_model_configs:
        :type app_model_configs: list[AppModelConfig]
        :raises ValueError:
        :raises TypeError:
        """
        if len(app_model_configs) == 0:
            raise ValueError(
                "APP_MODEL_CONFIGS must contain at least one App/Model"
            )

        bads = [
            config
            for config in app_model_configs
            if not isinstance(config, dict)
        ]
        if bads:
            raise TypeError(
                "APP_MODEL_CONFIGS must contains only dicts: {}".format(
                    str(bads)[1:-1]
                )
            )


# pipe call  ===================================================================
PIPE_USER_ROLE = "user"  # key in body


class _PipeCallBody(BaseModel):

    stream: Optional[bool] = Field(default=False)
    model: str
    messages: list[dict[str, str]] = Field(min_length=1)


class _PipeCallUser(BaseModel):

    id: Optional[str] = Field(default="user")
    email: Optional[str] = Field(default="")
    username: Optional[str] = Field(default="")
    name: Optional[str] = Field(default="")


class _PipeCallMetadata(BaseModel):
    pass


class PipeCall(BaseModel):  # **************************************************
    """
    a wrapper class containing all infos of a single OWU Pipe Function request,
    i.e. a single call from Pipe.pipe()
    """

    # Fields  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    body: _PipeCallBody
    user: _PipeCallUser
    metadata: _PipeCallMetadata
    message: str = ""  # placeholder

    # Public Properties  +++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @computed_field(return_type=str)
    @property
    def username(self):
        """
        :return:
        :rtype: str
        """
        return (
            self.user.name
            or self.user.username
            or self.user.email
            or self.user.id
        )

    @computed_field(return_type=str)
    @property
    def model_id(self):
        """
        :return: model id required by this call
        :rtype: str
        """
        full_model_id = self.body.model
        model_id = full_model_id.rsplit(".", 1)[-1]
        return model_id

    # post-init  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def model_post_init(self, __context):  # pylint: disable=arguments-differ
        for section in reversed(self.body.messages):
            if section["role"] == PIPE_USER_ROLE:
                self.message = section["content"]
                return

        raise ValueError("missing {} message in body".format(PIPE_USER_ROLE))


# Dify side  ###################################################################
# Dify constants  ==============================================================
REQUEST_TIMEOUT = 30
STREAM_REQUEST_TIMEOUT = 300
CONNECTION_ERR_MSG = "fail to connect Dify: "


# Dify helpers  ================================================================


class DifyAppType(Enum):
    """
    type of Dify App, either Workflow or Chatflow (multi-round)

    value of enums are identical to
    those appear in /info response of Dify Backend API
    """

    WORKFLOW = "workflow"
    CHATFLOW = "advanced-chat"  # multi-turn chats


class StreamResponse:  # =======================================================

    pass


class BaseDifyApp:  # ==========================================================
    """
    logic container representing an **App** in Dify,
    handling Dify Backend API side's logic
    (create payload satisfying Dify's syntax, etc.)


    :param config:
    :type config: AppModelConfig
    :param info_response:
    :type info_response: dict
    """

    # abstract method  *********************************************************

    @property
    def _chat_endpoint(self):
        """
        :return: url for accessing endpoint for LLM chatting
        :rtype: str
        """
        raise NotImplementedError

    @property
    def _chat_payload(self):
        """
        :return: payload data (json-dumped) sent to Dify during chat request
        :rtype: str
        """
        raise NotImplementedError

    # Public Methods  **********************************************************

    @classmethod
    def create_app(cls, config):
        """
        create an app of ``WorkflowApp`` or ``ChatflowApp``,
        getting app type and name by GET /info of Dify Backend API


        :param config:
        :type config: AppModelConfig
        :return: created app
        :rtype: WorkflowApp or ChatflowApp
        :raises ConnectionError:
        :raises ValueError:
        """
        # get app type & name  -------------------------------------------------
        # by accessing Dify /info
        try:
            response_object = requests.get(
                cls._info_endpoint,
                headers=cls._create_http_header(config),
                timeout=REQUEST_TIMEOUT,
            )
            response_object.raise_for_status()
            info_response = response_object.json()

        except requests.exceptions.RequestException as err:
            raise ConnectionError(CONNECTION_ERR_MSG + err.args[0]) from err

        # parse App type  ------------------------------------------------------
        try:
            app_type = DifyAppType(info_response["mode"])
        except (KeyError, ValueError) as err:
            raise ValueError(
                "missing App Type (missing 'mode') from Dify: {}".format(
                    info_response
                )
            ) from err

        # create app  ----------------------------------------------------------
        if app_type == DifyAppType.WORKFLOW:
            return WorkflowApp(config, info_response)
        else:
            return ChatflowApp(config, info_response)

    def reply(self):
        pass  # Todo

    def open_chat_response(self):  # FIXME
        """
        open a `Response` object connecting to Dify for replying


        :return: Response object
        :rtype: requests.Response
        :raises ConnectionError:
        """
        try:
            timeout = (
                STREAM_REQUEST_TIMEOUT
                if self.current_enable_stream
                else REQUEST_TIMEOUT
            )
            response_obj = requests.post(
                self.main_url,
                headers=self.http_header,
                data=self._create_reply_payload(),
                stream=self.current_enable_stream,
                timeout=timeout,
            )
            response_obj.raise_for_status()
            return response_obj

        # handle network errors
        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail request to Dify: {}".format(err.args[0])
            ) from err

    # constructor  *************************************************************

    def __init__(self, config, info_response):
        self.config = config

        self.response_name = (
            info_response["name"] if "name" in info_response else None
        )

        self.model = None  # must to be assigned

    # private properties  ******************************************************

    # url for accessing ``/info`` endpoint
    _info_endpoint = DIFY_BACKEND_API_BASE_URL + "/info"

    # private method  **********************************************************

    @staticmethod
    def _create_http_header(config, enable_stream=False):
        """
        :param config:
        :type config: AppModelConfig
        :param enable_stream:
        :type enable_stream: bool, optional
        :return: create a http header object provided to `requests.get/.post`
        :rtype: dict
        """
        header_dict = {
            "Authorization": "Bearer {}".format(config.key),
            "Content-Type": "application/json",
        }

        if enable_stream:
            header_dict["Accept"] = "text/event-stream"

        return header_dict

    @property
    def _http_header(self):
        """
        :return: http header object for current round
        :rtype: dict
        """
        return self._create_http_header(
            self.config, enable_stream=self.model.is_using_stream
        )

    @property
    def _response_mode(self):
        """
        :return: "streaming" or "blocking", used in request payload
        :rtype: str
        """
        return "streaming" if self.model.is_using_stream else "blocking"

    # magic methods  ***********************************************************

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__, self.response_name or self.config.model_id
        )


class WorkflowApp(BaseDifyApp):  # =============================================
    """
    representing a Workflow App in Dify


    :param config:
    :type config: AppModelConfig
    :param info_response:
    :type info_response: dict
    """

    # implement BaseDifyApp  ***************************************************

    @property
    def _chat_endpoint(self):
        return DIFY_BACKEND_API_BASE_URL + "/workflows/run"

    @property
    def _chat_payload(self):
        payload_dict = {
            "inputs": {
                self.config.query_input_field_identifier: (
                    self.model.call.message
                )
            },
            "response_mode": self._response_mode,
            "user": "user",  # Todo read from config
        }

        return json.dumps(payload_dict)


class ChatflowApp(BaseDifyApp):  # =============================================
    """
    representing a Chatflow App in Dify


    :param config:
    :type config: AppModelConfig
    :param info_response:
    :type info_response: dict
    """

    # implement BaseDifyApp  ***************************************************

    @property
    def _chat_endpoint(self):
        return DIFY_BACKEND_API_BASE_URL + "/chat-messages"

    @property
    def _chat_payload(self):
        payload_dict = {
            "query": self.model.call.message,
            "response_mode": self._response_mode,
            "user": "user",  # Todo
            "conversation_id": "",  # Todo
            "auto_generate_name": False,
            "inputs": {},
        }
        return json.dumps(payload_dict)


# OWU side  ####################################################################
# OWU constants  ===============================================================


class OWUModel:  # =============================================================
    """
    logic & data container representing a single pipe **model** in Open WebUI,
    handling OWU side's logic (parse `body`, etc.)


    :param config:
    :type config: AppModelConfig
    :param app:
    :type app: Workflow or Chatflow
    """

    # Public Method  ***********************************************************

    def reply(self, call):
        """
        :param call:
        :type call: PipeCall
        :return: the response of current round
        :rtype: str or StreamResponse
        """
        # Todo make file upload
        self.call = call

        return self.app.reply()

    @property
    def is_using_stream(self):
        """
        :return: whether using stream during replying in current round
        :rtype: bool
        """
        return (not self.config.disallows_streaming) and self.call.body.stream

    # constructor  *************************************************************

    def __init__(self, config, app):
        self.config = config
        self.app = app

        self.display_name = config.name or app.response_name or config.model_id

        # to be assigned
        self.call = None


class Pipe:  # =================================================================
    """
    Pipe class required by OWU Pipe Function


    :raises ValueError:
    :raises TypeError:
    :raises ConnectionError:
    :raises pydantic.ValidationError:
    """

    class Valves(BaseModel):  # pylint: disable=missing-class-docstring
        pass  # configuration via Python constants

    def __init__(self):
        AppModelConfig.validate_app_model_configs(APP_MODEL_CONFIGS)

        # create models & apps  ------------------------------------------------
        self.models = {}
        self.apps = {}
        for config_dict in APP_MODEL_CONFIGS:
            # create config
            config = AppModelConfig.model_validate(config_dict)

            # create model & app
            app = BaseDifyApp.create_app(config)
            model = OWUModel(config, app)

            # connect model & app
            app.model = model

            # save model & app
            model_id = config.model_id
            self.models[model_id] = model
            self.apps[model_id] = app

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
            {"id": model_id, "name": model.display_name}
            for model_id, model in self.models.items()
        ]

    async def pipe(self, body, __user__, __metadata__):
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
        if DEBUG_PIPE_DIRECT_RESPONSE:
            return self._generate_pipe_direct_response(
                body, __user__, __metadata__
            )

        owu_call = PipeCall(body=body, user=__user__, metadata=__metadata__)

        # Bug keeps sending chat to the same chat id, when use from continue
        model = self.models.get(owu_call.model_id)
        if model is None:
            raise ValueError(
                "missing model with model_id: {}".format(owu_call.model_id)
            )

        return model.reply(owu_call)

    # private method  **********************************************************

    @staticmethod
    def _generate_pipe_direct_response(body, user, metadata):
        return """## `body`

    ```json
    {}
    ```

    ## `__user__`

    ```json
    {}
    ```

    ## `__metadata__`

    ```json
    {}
    ```
    """.format(
            json.dumps(body, indent=2),
            json.dumps(user, indent=2),
            json.dumps(metadata, indent=2),
        )
