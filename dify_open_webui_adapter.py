# todo docstring for this script

import json

from pydantic import BaseModel, Field
import requests

__version__ = "1.0.0-alpha"
__author__ = "kamiLeL"


ENABLE_DEBUG = True
REQUEST_TIMEOUT = 30


class Pipe:
    class Valves(BaseModel):
        DIFY_BACKEND_API_BASE_URL: str = Field(
            default="https://api.dify.ai/v1",
            description="base URL to access Dify Backend Service API",
        )
        DIFY_API_KEY: str = Field(
            default="",
            description="secret key to access Dify Backend Service API",
        )
        DIFY_WORKFLOW_ID: str = Field(
            default="", description="id of the specific Dify workflow"
        )
        OWU_MODEL_ID: str = Field(
            default="dify-open-webui-adapter-model",
            description="model id as it appears in Open WebUI",
        )
        OWU_MODEL_NAME: str = Field(
            default="Dify-Open Webui Adapter Model",
            description="model name as it appears in Open WebUI",
        )

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body):
        self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL
        self.api_key = self.valves.DIFY_API_KEY
        self.workflow_id = self.valves.DIFY_WORKFLOW_ID

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

        if ENABLE_DEBUG:
            debug_lines.append("## user message")
            debug_lines.append(message)

        # send request to Dify
        # FIXME use try to catch request error

        response = requests.post(
            self._gen_request_url(),
            headers=self._gen_headers(),
            data=self._build_payload(message, body),
            timeout=REQUEST_TIMEOUT,
        )
        if ENABLE_DEBUG:
            debug_lines.append("## request url")
            debug_lines.append(self._gen_request_url())
            debug_lines.append("## headers")
            debug_lines.append(repr(self._gen_headers()))
            debug_lines.append("## payloads")
            debug_lines.append(repr(self._build_payload(message, body)))

        # parse returned data
        # FIXME error handling for non-200 response
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

        if ENABLE_DEBUG:
            debug_lines.append("\n\n----\n\n\n")
            debug_lines.append(output)
            return "\n".join(debug_lines)
        else:
            return output

    def pipes(self):
        return [{
            "id": self.valves.OWU_MODEL_ID,
            "name": self.valves.OWU_MODEL_NAME,
        }]

    def _gen_request_url(self):
        return "{}/workflows/{}/run".format(self.base_url, self.workflow_id)

    def _gen_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.api_key),
            "Content-Type": "application/json",
        }

    def _build_payload(self, message, everything):
        inputs = {"input": message}
        if ENABLE_DEBUG:
            inputs["everything"] = repr(everything)

        payload_dict = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": "user",
        }
        return json.dumps(payload_dict)
