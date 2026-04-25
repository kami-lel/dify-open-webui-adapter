# Hack rm


# end of config  ###############################################################

# pylint: disable=wrong-import-position
from enum import Enum, Flag, auto
import json
from json import JSONDecodeError

from pydantic import BaseModel

# constants  ===================================================================
DEFINED_APP_MODEL_CONFIG_KEYS = (
    "key",
    "model_id",
    "name",
    "query_input_field_identifier",
    "reply_output_variable_identifier",
    "disallows_streaming",
)

# Dify constants  **************************************************************
DEFAULT_QUERY_INPUT_FIELD_IDENTIFIER = "query"
DEFAULT_REPLY_OUTPUT_VARIABLE_IDENTIFIER = "answer"


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

        opt = self.app.reply()

        return opt


# Dify side  ###################################################################
class BaseDifyApp:
    """
    logic container representing an **App** in Dify,
    handling Dify Backend API side's logic
    (create payload satisfying Dify's syntax, etc.)


    :param model:
    :type model: OWUModel
    """

    def reply(self):
        """
        handle Dify side of processing per-round response of conversation,
        by requesting Dify Backend API


        :raises ConnectionError:
        :raises KeyError:
        :return: the response
        :rtype: str or Iterable
        """
        if not self.disallows_streaming and self.current_enable_stream:
            return _StreamingConversationRound(self)
        else:
            return self._reply_blocking()

    def open_reply_response(self):
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

    # abstract methods  ========================================================

    @property
    def main_url(self):
        """
        :return: endpoint URL to access Dify
        :rtype: str
        """
        raise NotImplementedError

    def _reply_blocking(self):
        """
        :return: the response
        :rtype: str
        """
        raise NotImplementedError

    def _create_reply_payload(self):
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

        # current conversations  -----------------------------------------------
        self.current_user_msg_content = ""


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

    def _reply_blocking(self):
        """
        :raises ConnectionError:
        :raises KeyError:
        """
        response_object = self.open_reply_response()
        response = response_object.json()

        try:
            return response["data"]["outputs"][self.reply_identifier]

        except KeyError as err:
            raise KeyError(
                "miss key in Dify response: {}".format(err.args[0])
            ) from err

        finally:
            response_object.close()

    def _create_reply_payload(self):
        payload_dict = {
            "inputs": {
                self.query_identifier: self.current_user_msg_content,
                **self.input_fields,
            },
            "response_mode": (
                "streaming" if self.current_enable_stream else "blocking"
            ),
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

    def _reply_blocking(self):
        """
        :raises ConnectionError:
        :raises KeyError:
        """
        response_object = self.open_reply_response()
        response = response_object.json()

        try:
            if not self.conversation_id:  # 1st round of this conversation
                self.conversation_id = response["conversation_id"]

            return response["answer"]

        except KeyError as err:
            raise KeyError(
                "miss key in Dify response: {}".format(err.args[0])
            ) from err

        finally:
            response_object.close()

    def _create_reply_payload(self):
        payload_dict = {
            "query": self.current_user_msg_content,
            "response_mode": (
                "streaming" if self.current_enable_stream else "blocking"
            ),
            "user": DIFY_USER_ROLE,
            "conversation_id": self.conversation_id,
            "auto_generate_name": False,
            "inputs": {},
        }
        return json.dumps(payload_dict)


# helper class  ================================================================


class _SSEType(Flag):
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

    def __bool__(self):
        """
        :return: whether event is a relevant event
        :rtype: bool
        """
        return self != self.IRRELEVANT


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

    def __init__(self, app):
        self.app = app
        # cache the response for closing when finished this round
        self.response = self.app.open_reply_response()
        self.iter_lines = self.response.iter_lines()

    # implement iter()  ========================================================

    def __iter__(self):
        return self  # make self an Iterator

    def __next__(self):
        debug_lines = ["\n"]

        text = None
        event = _SSEType.IRRELEVANT  # default

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
                    event = _SSEType[event_value]
                except KeyError:  # not a relevant event
                    continue

                # extract text
                if event is _SSEType.message:
                    text = data["answer"]
                elif event is _SSEType.text_chunk:
                    text = data["data"]["text"]

                # extract conversation_id for Chatflow, if it's empty
                if (
                    isinstance(self.app, ChatflowApp)
                    and not self.app.conversation_id
                ):
                    self.app.conversation_id = data["conversation_id"]

            except StopIteration as err:
                raise ValueError(
                    "exhaust text/event-stream without ending event"
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
                    "miss key in text/event-stream content: {}".format(str(err))
                ) from err

        # an relevant event is found  ------------------------------------------

        if event in _SSEType.IS_END:  # end of current respond
            if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
                debug_lines.insert(1, "# LAST PASS")
                return "\n\n".join(debug_lines)

            self.response.close()
            raise StopIteration

        if DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE:
            debug_lines.insert(1, "# PASS")
            return "\n\n".join(debug_lines)

        # a text chunk as part of current respond
        return text


class Pipe:  ###################################################################

    def __init__(
        self,
        app_model_configs_override=None,
        base_url_override=None,
        skip_get_app_type_and_name=False,
    ):
        base_url = base_url_override or DIFY_BACKEND_API_BASE_URL
        app_model_configs = app_model_configs_override or APP_MODEL_CONFIGS

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
