# todo docstring for this script

from enum import Enum, auto
import json

from pydantic import BaseModel, Field
import requests

__version__ = "1.0.1-alpha"
__author__ = "kamiLeL"


class DIFY_APP(Enum):
    CHATFLOW = auto()
    WORKFLOW = auto()


DIFY_APP_TYPE = DIFY_APP.WORKFLOW
REQUEST_TIMEOUT = 30
ENABLE_DEBUG = False


class Pipe:
    class Valves(BaseModel):
        DIFY_BACKEND_API_BASE_URL: str = Field(
            default="https://api.dify.ai/v1",
            description="base URL to access Dify Backend Service API",
        )
        DIFY_APP_ID_1: str = Field(
            default="",
            description="id of specific version of 1st Dify app",
        )
        DIFY_API_KEY_1: str = Field(
            default="",
            description=(
                "Dify Backend Service API secret key to access 1st Dify app"
            ),
        )
        OWU_MODEL_ID_1: str = Field(
            default="",
            description="model id as it is used in Open WebUI of 1st Dify app",
        )
        OWU_MODEL_NAME_1: str = Field(
            default="",
            description=(
                "model name as it appears in Open WebUI of 1st Dify app,"
                " optional"
            ),
        )
        DIFY_APP_ID_2: str = Field(default="")
        DIFY_API_KEY_2: str = Field(default="")
        OWU_MODEL_ID_2: str = Field(default="")
        OWU_MODEL_NAME_2: str = Field(default="")
        DIFY_APP_ID_3: str = Field(default="")
        DIFY_API_KEY_3: str = Field(default="")
        OWU_MODEL_ID_3: str = Field(default="")
        OWU_MODEL_NAME_3: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()
        self.base_url = None
        self.models = {}

    def pipe(self, body):
        self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL

        debug_lines = []

        # get user's input
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
        app_id, api_secret_key = self.models[model_id]

        if ENABLE_DEBUG:
            debug_lines.append("## user message")
            debug_lines.append(message)
            debug_lines.append("## model id")
            debug_lines.append(model_id)
            debug_lines.append("## app id")
            debug_lines.append(app_id)
            debug_lines.append("## api secret key")
            debug_lines.append(api_secret_key)

        # send request to Dify
        url = self._gen_request_url(app_id)
        headers = self._gen_headers(api_secret_key)
        payloads = self._build_payload(message, body)

        try:
            response = requests.post(
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
            debug_lines.append("## request url")
            debug_lines.append(url)
            debug_lines.append("## headers")
            debug_lines.append(repr(headers))
            debug_lines.append("## payloads")
            debug_lines.append(repr(payloads))

        # parse returned data
        content = response.json()

        try:
            output = content["data"]["outputs"]["output"]
        except (KeyError, IndexError) as err:
            raise ValueError(
                "fail to parse response {}: {}".format(content, err)
            ) from err

        if ENABLE_DEBUG:
            debug_lines.append("## response content")
            debug_lines.append(repr(content))
            debug_lines.append("\n\n----\n\n\n")
            debug_lines.append(output)

        if ENABLE_DEBUG:
            return "\n".join(debug_lines)
        else:
            return output

    def pipes(self):
        apps = [
            self.valves.DIFY_APP_ID_1,
            self.valves.DIFY_APP_ID_2,
            self.valves.DIFY_APP_ID_2,
        ]
        keys = [
            self.valves.DIFY_API_KEY_1,
            self.valves.DIFY_API_KEY_2,
            self.valves.DIFY_API_KEY_3,
        ]
        models = [
            self.valves.OWU_MODEL_ID_1,
            self.valves.OWU_MODEL_ID_2,
            self.valves.OWU_MODEL_ID_3,
        ]
        names = [
            self.valves.OWU_MODEL_NAME_1,
            self.valves.OWU_MODEL_NAME_2,
            self.valves.OWU_MODEL_NAME_3,
        ]

        opt = []
        # add models only when given: app id, api key, and model id
        for app, key, model, name in zip(apps, keys, models, names):
            if app and key and model:
                # use model id when model name is not given
                opt_entry = {"id": model, "name": name or model}
                opt.append(opt_entry)

                # save model data
                self.models[model] = [app, key]

        return opt

    def _gen_request_url(self, app_id):
        return "{}/workflows/{}/run".format(self.base_url, app_id)

    def _gen_headers(self, api_secret_key):
        return {
            "Authorization": "Bearer {}".format(api_secret_key),
            "Content-Type": "application/json",
        }

    def _build_payload(self, message, everything_for_debug):
        inputs = {"input": message}
        if ENABLE_DEBUG:
            inputs["everything_for_debug"] = repr(everything_for_debug)

        payload_dict = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": "user",
        }
        return json.dumps(payload_dict)
