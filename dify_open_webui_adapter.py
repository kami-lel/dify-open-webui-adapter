# Todo docstring for this script
# Bug chatflow not working, only 1st message is repeated sent
# Fixme dont use 3 pipes

from enum import Enum
import json

from pydantic import BaseModel, Field
import requests

__version__ = "1.1.1-alpha"
__author__ = "kamiLeL"


class DIFY_APP_TYPE_ENUM(Enum):
    WORKFLOW = 0
    CHATFLOW = 1


REQUEST_TIMEOUT = 30
USER_ROLE = "user"
ENABLE_DEBUG = False


class Pipe:
    class Valves(BaseModel):
        DIFY_BACKEND_API_BASE_URL: str = Field(
            default="https://api.dify.ai/v1",
            description="base URL to access Dify Backend Service API",
        )
        # settings for Dify App  -----------------------------------------------
        DIFY_API_KEY: str = Field(
            default="",
            description=(
                "Dify Backend Service API secret key to access Dify app"
            ),
        )
        DIFY_APP_TYPE: int = Field(
            default=0,
            description="type of the Dify app, 0=Workflow, 1=Chatflow",
        )
        OWU_MODEL_ID: str = Field(
            default="",
            description="model id as it is used in Open WebUI of Dify app",
        )
        OWU_MODEL_NAME: str = Field(
            default="",
            description=(
                "model name as it appears in Open WebUI of Dify app, optional"
            ),
        )

    def __init__(self):
        self.valves = self.Valves()
        self.base_url = None
        self.model_data = {}  # locally saving model-related data
        self.debug_lines = []

    def pipe(self, body):
        self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL

        self.debug_lines = []

        # retrieve user input  -------------------------------------------------
        message = ""
        try:
            for msg in body["messages"]:
                if msg["role"] == "user":
                    message = msg["content"]
                    break

            if not message:
                raise ValueError(
                    "fail to find 'user' after exhausting 'messages'"
                )

        except (KeyError, IndexError, ValueError) as err:
            raise ValueError(
                "fail to get user message from body {}: {}".format(body, err)
            ) from err

        # Extract model id from the model name
        model_id = body["model"][body["model"].find(".") + 1 :]
        api_secret_key, app_type, conversation_id = self.model_data[model_id]

        if ENABLE_DEBUG:
            self.debug_lines.append("## body")
            self.debug_lines.append(repr(body))
            self.debug_lines.append("## user message")
            self.debug_lines.append(message)
            self.debug_lines.append("## model id")
            self.debug_lines.append(model_id)
            self.debug_lines.append("## api secret key")
            self.debug_lines.append(api_secret_key)
            self.debug_lines.append("## conversation id")
            self.debug_lines.append(conversation_id)

        # send request to Dify  ------------------------------------------------
        url = self._gen_request_url(app_type)
        headers = self._gen_headers(api_secret_key, app_type)
        payloads = self._build_payload(
            message, app_type, conversation_id, everything_for_debug=body
        )

        try:
            response_json = requests.post(
                url,
                headers=headers,
                data=payloads,
                timeout=REQUEST_TIMEOUT,
            )
        except Exception as err:
            raise ConnectionError(
                "fail to request POST:{}".format(err)
            ) from err

        if ENABLE_DEBUG:
            self.debug_lines.append("## request url")
            self.debug_lines.append(url)
            self.debug_lines.append("## headers")
            self.debug_lines.append(str(headers))
            self.debug_lines.append("## payloads")
            self.debug_lines.append(str(payloads))

        # output  --------------------------------------------------------------
        response_json = response_json.json()

        if ENABLE_DEBUG:
            self.debug_lines.append("## response content")
            self.debug_lines.append(repr(response_json))

        output = self._extract_output(
            model_id, response_json, app_type, conversation_id
        )

        if ENABLE_DEBUG:
            self.debug_lines.append("\n\n----\n\n\n")
            self.debug_lines.append(output)

        if ENABLE_DEBUG:
            return "\n".join(self.debug_lines)
        else:
            return output

    def pipes(self):
        keys = [
            self.valves.DIFY_API_KEY,
            self.valves.DIFY_API_KEY_2,
            self.valves.DIFY_API_KEY_3,
        ]
        app_types = [
            self.valves.DIFY_APP_TYPE,
            self.valves.DIFY_APP_TYPE_2,
            self.valves.DIFY_APP_TYPE_3,
        ]
        models = [
            self.valves.OWU_MODEL_ID,
            self.valves.OWU_MODEL_ID_2,
            self.valves.OWU_MODEL_ID_3,
        ]
        names = [
            self.valves.OWU_MODEL_NAME,
            self.valves.OWU_MODEL_NAME_2,
            self.valves.OWU_MODEL_NAME_3,
        ]

        opt = []
        # add models only when given: api key, app type, and model id
        for key, app_type, model, name in zip(keys, app_types, models, names):
            try:  # convert to enum
                app_type_enum = DIFY_APP_TYPE_ENUM(app_type)
            except ValueError:
                app_type_enum = None

            if key and app_type_enum and model:
                # use model id when model name is not given
                opt_entry = {"id": model, "name": name or model}
                opt.append(opt_entry)

                # save model data
                self.model_data[model] = [key, app_type_enum, ""]

        return opt

    # generate and build request  ##############################################

    def _gen_request_url(self, app_type):
        if app_type == DIFY_APP_TYPE_ENUM.WORKFLOW:
            return "{}/workflows/run".format(self.base_url)
        else:  # Chatflow
            return "{}/chat-messages".format(self.base_url)

    def _gen_headers(self, api_secret_key, app_type):
        return {
            "Authorization": "Bearer {}".format(api_secret_key),
            "Content-Type": "application/json",
        }

    def _build_payload(
        self, message, app_type, conversation_id, *, everything_for_debug
    ):
        everything_for_debug = str(everything_for_debug)

        if app_type == DIFY_APP_TYPE_ENUM.WORKFLOW:
            payload = self._build_payload_workflow(
                message, everything_for_debug
            )
        else:  # Chatflow
            payload = self._build_payload_chatflow(
                message, conversation_id, everything_for_debug
            )

        return json.dumps(payload)

    def _extract_output(
        self, model_id, response_json, app_type, conversation_id
    ):
        if app_type == DIFY_APP_TYPE_ENUM.WORKFLOW:
            return self._extract_output_workflow(response_json)
        else:  # chatflow
            return self._extract_output_chatflow(
                model_id, response_json, conversation_id
            )

    # Workflow specific  #######################################################

    def _build_payload_workflow(self, message, everything_for_debug):
        inputs = {"input": message}
        if ENABLE_DEBUG:
            inputs["everything_for_debug"] = everything_for_debug

        payload_dict = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": USER_ROLE,
        }

        return payload_dict

    def _extract_output_workflow(self, response_json):
        try:
            output = response_json["data"]["outputs"]["output"]
        except (KeyError, IndexError) as err:
            raise ValueError(
                "fail to parse response {}: {}".format(response_json, err)
            ) from err

        return output

    # Chatflow specific  #######################################################

    def _build_payload_chatflow(
        self, message, conversation_id, everything_for_debug
    ):
        inputs = {}
        if ENABLE_DEBUG:
            inputs["everything_for_debug"] = everything_for_debug

        return {
            "inputs": inputs,
            "query": message,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": USER_ROLE,
            "auto_generate_name": False,
        }

    def _extract_output_chatflow(
        self, model_id, response_json, saved_conversation_id
    ):
        try:
            output = response_json["answer"]

            # save returned conversation idea for future rounds
            if not saved_conversation_id:
                conversation_id = response_json["conversation_id"]
                self.model_data[model_id][2] = conversation_id

                if ENABLE_DEBUG:
                    conversation_id = response_json["conversation_id"]
                    self.model_data[model_id][2] = conversation_id
                    self.debug_lines.append("## returned conversation id")
                    self.debug_lines.append(conversation_id)

        except (KeyError, IndexError) as err:
            raise ValueError(
                "fail to parse chatflow response {}: {}".format(
                    response_json, err
                )
            ) from err

        return output
