"""
Integrate Open WebUI and Dify by exposing a Dify App
(Workflow or Chatflow) as Open WebUI model using Open WebUI's Pipe Functions.

Supported Open WebUI Version:   v0.7.1
Supported Dify Version:         1.11.2

Q.v. ``https://github.com/kami-lel/dify-open-webui-adapter``
"""

# Bug keeps sending chat to the same chat id, when use from continue
# Bug fail to do pass thru
# Todo make file upload

# adapter version
__version__ = "2.2.1-alpha"
__author__ = "kamiLeL"


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"

APP_MODEL_CONFIGS = []

# end of config  ###############################################################

# pylint: disable=wrong-import-position
import uuid
from enum import Enum, Flag, auto
import json
from json import JSONDecodeError

from pydantic import BaseModel
import requests

# constants  ===================================================================
# Todo read user role from metadata
OWU_USER_ROLE = "user"
REQUEST_TIMEOUT = 30
STREAM_REQUEST_TIMEOUT = 300
DEFINED_APP_MODEL_CONFIG_KEYS = (
    "key",
    "model_id",
    "name",
    "query_input_field_identifier",
    "reply_output_variable_identifier",
    "disallows_streaming",
)

# Dify constants  **************************************************************
DIFY_USER_ROLE = "user"
DEFAULT_QUERY_INPUT_FIELD_IDENTIFIER = "query"
DEFAULT_REPLY_OUTPUT_VARIABLE_IDENTIFIER = "answer"

# debug flags  *****************************************************************
DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE = False
DEBUG_PIPE_DIRECT_RESPONSE = False


# helper Enum  =================================================================
class DifyAppType(Enum):
    """
    type of Dify App, either Workflow or Chatflow (multi-round)
    """

    # value of enums are identical to them appearing
    # in Dify Backend API's /info response
    WORKFLOW = "workflow"
    CHATFLOW = "advanced-chat"  # multi-turn chats


# Open WebUI side  #############################################################
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

    # public methods  ==========================================================

    def get_model_id_and_name(self):
        """
        :return: an entry of this model,
                such that it can be served to ``Pipe.pipes()``
        :rtype: dict{str: str}
        """
        return {"id": self.model_id, "name": self.name}

    def reply(self, body, user, metadata):
        """
        handle OWU side of processing per-round response of conversation


        :param body: `body` given by OWU Pipe.pipe()
        :type body: dict
        :param user: `__user__` given by Pipe.pipe()
        :type user: dict
        :param metadata: `__metadata__` given by Pipe.pipe()
        :type metadata: dict
        :raises ConnectionError:
        :raises ValueError:
        :raises KeyError:
        :return: the response
        :rtype: str
        """

        # OWU side  ------------------------------------------------------------
        last_user_msg_content_content = self._get_last_user_msg_content(body)
        enable_stream = "stream" in body and bool(body["stream"])
        # Todo extract custom para from body

        # Dify side  -----------------------------------------------------------
        opt = self.app.reply(last_user_msg_content_content, enable_stream)

        return opt

    # constructor  =============================================================
    def __init__(
        self,
        base_url,
        app_model_config,
        *,
        skip_get_app_type_and_name=False,  # for debug & testing
        app_type_override=None,  # for debug & testing
    ):
        key, self.model_id, provided_name = self._parse_app_model_config_arg(
            app_model_config
        )

        if skip_get_app_type_and_name:
            self.app_type, response_name = app_type_override, None
        else:
            self.app_type, response_name = BaseDifyApp.get_app_type_and_name(
                base_url, key
            )

        # set self.name
        self.name = provided_name or response_name or self.model_id

        # create app
        if self.app_type == DifyAppType.WORKFLOW:
            self.app = WorkflowApp(self, base_url, app_model_config)
        else:
            self.app = ChatflowApp(self, base_url, app_model_config)

    # private methods  =========================================================

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

    def _get_last_user_msg_content(self, body):
        for section in reversed(body["messages"]):
            if section["role"] == OWU_USER_ROLE:
                return section["content"]

        raise ValueError("missing {} message in body".format(OWU_USER_ROLE))

    # magic methods  ===========================================================

    def __repr__(self):
        return "OWUModel({}:{})".format(self.name, repr(self.app))


# Dify side  ###################################################################
class BaseDifyApp:
    """
    logic container representing an **App** in Dify,
    handling Dify Backend API side's logic
    (create payload satisfying Dify's syntax, etc.)


    :param model:
    :type model: OWUModel
    """

    # public methods  ==========================================================

    @staticmethod
    def get_app_type_and_name(base_url, key):
        """
        get Dify App's Type & Name, by GET /info of Dicy Backend API


        :param base_url:
        :type base_url: str
        :param key:
        :type key: str
        :raises ConnectionError:
        :raises ValueError:
        :return: type & name of Dify App
        :rtype: tuple(str, DifyAppType)
        """
        info_url = "{}/info".format(base_url)

        # GET /info  -----------------------------------------------------------
        try:
            response_object = requests.get(
                info_url,
                headers=create_http_header(key, enable_stream=False),
                timeout=REQUEST_TIMEOUT,
            )
            response_object.raise_for_status()
            response = response_object.json()

        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail request to Dify: {}".format(err.args[0])
            ) from err

        # parse App type  ------------------------------------------------------
        try:
            app_type = DifyAppType(response["mode"])
        except (KeyError, ValueError) as err:
            raise ValueError("fail to get App Type from Dify") from err

        response_name = response["name"] if "name" in response else None

        return app_type, response_name

    def reply(self, last_user_msg_content, enable_stream):
        """
        handle Dify side of processing per-round response of conversation,
        by requesting Dify Backend API


        :raises ConnectionError:
        :raises KeyError:
        :return: the response
        :rtype: str or Iterable
        """
        return (
            _StreamingConversationRound(self, last_user_msg_content)
            if not self.disallows_streaming and enable_stream
            else self._reply_blocking(last_user_msg_content)
        )

    def http_header(
        self, enable_stream=False
    ):  # pylint: disable=missing-function-docstring
        return create_http_header(self.key, enable_stream=enable_stream)

    # abstract methods  ========================================================

    @property
    def main_url(self):
        """
        :return: endpoint URL to access Dify
        :rtype: str
        """
        raise NotImplementedError

    def _reply_blocking(self, last_user_msg_content):
        """
        :return: the response
        :rtype: str
        """
        raise NotImplementedError

    def _create_reply_payload(self, last_user_msg_content, enable_stream=False):
        """
        generate payload during .reply()


        :return: JSON-formatted request payload data,
                e.g. it can be feed to ``requests.post(data=~)``
        :rtype: str
        """
        raise NotImplementedError

    # constructor  =============================================================
    def __init__(self, model, base_url, config):
        self.model = model
        self.base_url = base_url
        self.key = config["key"]

        # allows streaming  ----------------------------------------------------
        self.disallows_streaming = False
        if "disallows_streaming" in config:
            self.disallows_streaming = config["disallows_streaming"]
            if not isinstance(self.disallows_streaming, bool):
                raise TypeError(
                    "entry in APP_MODEL_CONFIGS, "
                    + "value of 'disallows_streaming' must be bool: {}".format(
                        self.disallows_streaming
                    )
                )

    # private methods  =========================================================

    def _open_reply_response(self, last_user_msg_content, enable_stream=False):
        """
        open a `Response` object connecting to Dify during .reply()


        :return:
        :rtype: requests.Response
        :raises ConnectionError:
        """
        try:
            data = self._create_reply_payload(
                last_user_msg_content, enable_stream
            )
            headers = self.http_header(enable_stream)
            response_obj = requests.post(
                self.main_url,
                headers=headers,
                data=data,
                stream=enable_stream,
                timeout=(
                    STREAM_REQUEST_TIMEOUT if enable_stream else REQUEST_TIMEOUT
                ),
            )
            response_obj.raise_for_status()
            return response_obj

        # handle network errors
        except requests.exceptions.RequestException as err:
            raise ConnectionError(
                "fail request to Dify: {}\n{}".format(err.args[0], data)
            ) from err


class WorkflowApp(BaseDifyApp):
    """
    representing a Workflow App in Dify
    """

    # constructor  =============================================================
    def __init__(self, model, base_url, config):
        super().__init__(model, base_url, config)
        # read from config  ----------------------------------------------------
        self.query_identifier = config.get(
            "query_input_field_identifier",
            DEFAULT_QUERY_INPUT_FIELD_IDENTIFIER,
        )
        self.reply_identifier = config.get(
            "reply_output_variable_identifier",
            DEFAULT_REPLY_OUTPUT_VARIABLE_IDENTIFIER,
        )
        # read additional input fields
        self.input_fields = {
            k: v
            for k, v in config.items()
            if k not in DEFINED_APP_MODEL_CONFIG_KEYS
        }

    # implement BaseDifyApp  ===================================================

    @property
    def main_url(self):
        return "{}/workflows/run".format(self.base_url)

    def _reply_blocking(self, last_user_msg_content):
        """
        :raises ConnectionError:
        :raises KeyError:
        """
        response_object = self._open_reply_response(
            last_user_msg_content, False
        )
        response = response_object.json()

        try:
            return response["data"]["outputs"][self.reply_identifier]

        except KeyError as err:
            raise KeyError(
                "fail to parse Dify response, missing key: {}".format(
                    err.args[0]
                )
            ) from err

        finally:
            response_object.close()

    def _create_reply_payload(self, last_user_msg_content, enable_stream=False):
        payload_dict = {
            "inputs": {
                self.query_identifier: last_user_msg_content,
                **self.input_fields,
            },
            "response_mode": "streaming" if enable_stream else "blocking",
            "user": DIFY_USER_ROLE,
        }

        return json.dumps(payload_dict)


class ChatflowApp(BaseDifyApp):
    """
    representing a Chatflow App in Dify
    """

    # properties  ==============================================================

    @property
    def conversation_id(self):
        """
        :return: correct Dify ``conversation_id``
                (depends on OWU ``chat_id``);
                empty if a new conversation is required
        :rtype: str
        """
        if self.current_chat_id not in self.chat2conversation_ids:
            # waiting to be set
            self.chat2conversation_ids[self.current_chat_id] = ""

        return self.chat2conversation_ids[self.current_chat_id]

    @conversation_id.setter
    def conversation_id(self, value):
        self.chat2conversation_ids[self.current_chat_id] = value

    # constructor  =============================================================
    def __init__(self, model, base_url, config):
        super().__init__(model, base_url, config)
        self.current_chat_id = ""
        self.chat2conversation_ids = {}

    # implement BaseDifyApp  ===================================================

    @property
    def main_url(self):
        return "{}/chat-messages".format(self.base_url)

    def _reply_blocking(self, last_user_msg_content):
        """
        :raises ConnectionError:
        :raises KeyError:
        """
        response_object = self._open_reply_response(
            last_user_msg_content, False
        )
        response = response_object.json()

        try:
            if not self.conversation_id:  # 1st round of this conversation
                self.conversation_id = response["conversation_id"]

            return response["answer"]

        except KeyError as err:
            raise KeyError(
                "fail to parse Dify response, missing key: {}".format(
                    err.args[0]
                )
            ) from err

        finally:
            response_object.close()

    def _create_reply_payload(self, last_user_msg_content, enable_stream=False):
        payload_dict = {
            "query": last_user_msg_content,
            "response_mode": "streaming" if enable_stream else "blocking",
            "user": DIFY_USER_ROLE,
            "conversation_id": self.conversation_id,
            "auto_generate_name": False,
            "inputs": {},
        }
        return json.dumps(payload_dict)


# helper class  ================================================================


def create_http_header(key, enable_stream=False):
    """
    :param key:
    :type key: str
    :param enable_stream:
    :type enable_stream: bool, optional
    :return: http header object provided to `requests.get`
    :rtype: dict
    """
    header_dict = {
        "Authorization": "Bearer {}".format(key),
        "Content-Type": "application/json",
    }

    if enable_stream:
        header_dict["Accept"] = "text/event-stream"

    return header_dict


class _SSE(Flag):
    """
    represent a single **relevant** SSE specified by Dify Backend API
    """

    # pylint: disable=invalid-name

    # events we don't care about
    IRRELEVANT = 0

    # enum name specified by Dify Backend API
    text_chunk = auto()
    message = auto()
    workflow_finished = auto()
    message_end = auto()

    # events which indicate end of  current round response
    IS_END = workflow_finished | message_end


class _StreamingConversationRound:
    """
    represent a single conversation round with Dify


    :raises ValueError:
    :raises UnicodeDecodeError:
    :raises json.JSONDecodeError:
    :raises KeyError:
    """

    _TEXT_STREAM_ENCODING = "utf-8"
    _STREAM_PREFIX = "data: "
    # enable debug mode such it returns text-stream directly

    def __init__(self, app, last_user_msg_content):
        self.app = app
        self.response = self.app._open_reply_response(
            last_user_msg_content, True
        )
        self.iter_lines = self.response.iter_lines()
        self._debug_stop_on_next = False

    # implemetn iter()  ========================================================

    def __iter__(self):
        return self  # make self an Iterator

    def __next__(self):
        if self._debug_stop_on_next:
            raise StopIteration

        debug_lines = ["\n"]

        text = None
        event = _SSE.IRRELEVANT  # default

        # consume self.iter_lines until find relevant events
        while not event:
            try:
                raw = next(self.iter_lines)
                line = raw.decode(self._TEXT_STREAM_ENCODING)
                if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
                    debug_lines.append(line)

                # deal with data: prefix
                if not line.startswith(self._STREAM_PREFIX):
                    continue  # not start w/ "data: ", skip
                line = line[len(self._STREAM_PREFIX) :]

                # parse data as JSON
                data = json.loads(line)
                event_value = data["event"]

                # deal with only relevant types of SSE
                try:
                    event = _SSE[event_value]
                except KeyError:  # not a relevant event
                    continue

                # extract text
                if event is _SSE.message:
                    text = data["answer"]
                elif event is _SSE.text_chunk:
                    text = data["data"]["text"]

                # extract conversation_id for Chatflow, if it's empty
                if (
                    isinstance(self.app, ChatflowApp)
                    and not self.app.conversation_id
                ):
                    self.app.conversation_id = data["conversation_id"]

            except StopIteration as err:
                raise ValueError(
                    "exhaust text/event-stream "
                    "but detect no events indicating finishing"
                ) from err

            except UnicodeDecodeError as err:
                err.args = (
                    "fail to decode text/event-stream: {}".format(str(err)),
                    *(err.args[1:]),
                )
                raise  # re-raise

            except JSONDecodeError as err:
                err.args = (
                    "fail to parse text/event-stream as JSON: {}: {}".format(
                        err.args[0], raw
                    ),
                    *(err.args[1:]),
                )
                raise  # re-raise

            except KeyError as err:
                raise KeyError(
                    "missing key in text/event-stream content: {}".format(
                        str(err)
                    )
                ) from err

        # an relevant event is found
        if event in _SSE.IS_END:  # end of current respond
            if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
                self._debug_stop_on_next = True
                debug_lines.insert(1, "# LAST PASS")
                return "\n\n".join(debug_lines)

            self.response.close()
            raise StopIteration

        if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
            debug_lines.insert(1, "# PASS")
            return "\n\n".join(debug_lines)

        # a text chunk as part of current respond
        return text


# Pipe class required by OWU  ##################################################
class Pipe:  # pylint: disable=missing-class-docstring

    class Valves(BaseModel):
        pass  # configuration via Python constants

    def __init__(
        self,
        app_model_configs_override=None,
        base_url_override=None,
        skip_get_app_type_and_name=False,
    ):
        base_url = base_url_override or DIFY_BACKEND_API_BASE_URL
        app_model_configs = app_model_configs_override or APP_MODEL_CONFIGS

        _check_app_model_configs_structure(app_model_configs)

        # populate containers   ------------------------------------------------
        self.model_containers = {}
        for config in app_model_configs:
            model = OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=skip_get_app_type_and_name,
            )
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
            return _generate_pipe_direct_response(body, __user__, __metadata__)

        if "model" not in body:
            raise IndexError("missing entry 'model' in body")

        # extract model_id from body
        model_id = body["model"][body["model"].find(".") + 1 :]
        opt = self.model_containers[model_id].reply(
            body, __user__, __metadata__
        )

        return opt


# helper methods  ==============================================================
def _check_app_model_configs_structure(app_model_configs):
    if len(app_model_configs) == 0:
        raise ValueError(
            "APP_MODEL_CONFIGS must contain at least one App/Model"
        )

    bads = tuple(
        config for config in app_model_configs if not isinstance(config, dict)
    )
    if bads:
        raise ValueError(
            "APP_MODEL_CONFIGS must contains only dicts: {}".format(bads)
        )


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
