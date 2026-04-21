"""
Integrating between: Open WebUI (abbr OWU) and Dify,
by exposing a Dify **app** (supporting Workflow and Chatflow)
as Open WebUI **model**.

Connecting with Dify app via *Dify Backend API*
and with OWU via *Pipe Function*.

Q.v. ``https://github.com/kami-lel/dify-open-webui-adapter``
"""

# adapter version
__version__ = "2.2.1-alpha"
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
from typing import Optional
import requests

from pydantic import BaseModel, Field


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

    # Public Methods ***********************************************************

    @staticmethod
    def validate_app_model_configs(app_model_configs):
        """
        validate basic structure of ``APP_MODEL_CONFIGS``
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


class PipeRequest(BaseModel):  # ===============================================
    """
    a wrapper class containing all infos of a single OWU Pipe Function request,
    i.e. a single call from Pipe.pipe()
    """

    # fields  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    body: dict
    user: dict
    metadata: dict


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

    # Public Methods  **********************************************************

    @classmethod
    def create_app(cls, config):
        """
        TODO

        get Dify App's Type & Name, by GET /info of Dify Backend API


        :param config:
        :type config:
        :raises ConnectionError:
        :raises ValueError:
        """
        # get app type & name  -------------------------------------------------
        # by accessing Dify /info
        info_url = DIFY_BACKEND_API_BASE_URL + "/info"

        try:
            response_object = requests.get(
                info_url,
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
                "missing App Type ('mode') from Dify: {}".format(info_response)
            ) from err

        # create app  ----------------------------------------------------------
        if app_type == DifyAppType.WORKFLOW:
            return WorkflowApp(config, info_response)
        else:
            return ChatflowApp(config, info_response)

    # constructor  *************************************************************

    def __init__(self, config, info_response):
        self.config = config

        self.response_name = (
            info_response["name"] if "name" in info_response else None
        )

        self.model = None  # must to be assigned

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
            self.config.key, enable_stream=self.current_enable_stream
        )


class WorkflowApp(BaseDifyApp):  # =============================================

    pass


class ChatflowApp(BaseDifyApp):  # =============================================

    pass


# OWU side  ####################################################################
# OWU constants  ===============================================================


class OWUModel:  # =============================================================
    """
    logic & data container representing a single pipe **model** in Open WebUI,
    handling OWU side's logic (parse `body`, etc.)


    :param config:
    :type config: AppModelConfig
    """

    # constructor  *************************************************************

    def __init__(self, config):
        self.config = config
        self.app = None  # to be assigned


class Pipe:  # =================================================================
    """
    Pipe class required by OWU Pipe Function
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
            model = OWUModel(config)

            # connect model & app
            model.app = app
            app.model = model

            # save model & app
            model_id = model.model_id
            self.models[model_id] = model
            self.apps[model_id] = app

    def pipes(self):
        pass

    async def pipe(self, body, __user__, __metadata__):
        owu_request = PipeRequest(
            body=body, user=__user__, metadata=__metadata__
        )
