# todo docstring for this script

import json

from pydantic import BaseModel, Field
import requests

__version__ = "1.0.1-alpha"
__author__ = "kamiLeL"


ENABLE_DEBUG = False
REQUEST_TIMEOUT = 30


class Pipe:
    class Valves(BaseModel):
        DIFY_BACKEND_API_BASE_URL: str = Field(
            default="https://api.dify.ai/v1",
            description="base URL to access Dify Backend Service API",
        )
        DIFY_WORKFLOW_ID_1: str = Field(
            default="",
            description="id of specific version of 1st Dify workflow",
        )
        DIFY_API_KEY_1: str = Field(
            default="",
            description=(
                "Dify Backend Service API secret key "
                "to access 1st Dify workflow"
            ),
        )
        OWU_MODEL_ID_1: str = Field(
            default="",
            description=(
                "model id as it is used in Open WebUI of 1st Dify workflow"
            ),
        )
        OWU_MODEL_NAME_1: str = Field(
            default="",
            description=(
                "model name as it appears in Open WebUI of 1st Dify workflow,"
                " optional"
            ),
        )
        DIFY_WORKFLOW_ID_2: str = Field(default="")
        DIFY_API_KEY_2: str = Field(default="")
        OWU_MODEL_ID_2: str = Field(default="")
        OWU_MODEL_NAME_2: str = Field(default="")
        DIFY_WORKFLOW_ID_3: str = Field(default="")
        DIFY_API_KEY_3: str = Field(default="")
        OWU_MODEL_ID_3: str = Field(default="")
        OWU_MODEL_NAME_3: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()
        self.base_url = None

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

        if ENABLE_DEBUG:
            debug_lines.append("## user message")
            debug_lines.append(message)

        # send request to Dify
        # fixme use try to catch request error

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
        # fixme error handling for non-200 response
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
        workflows = [
            self.valves.DIFY_WORKFLOW_ID_1,
            self.valves.DIFY_WORKFLOW_ID_2,
            self.valves.DIFY_WORKFLOW_ID_2,
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
        # add models only when given: workflow id, api key, and model id
        for workflow, key, model, name in zip(workflows, keys, models, names):
            if workflow and key and model:
                # use model id when model name is not given
                entry = {"id": model, "name": name or model}
                opt.append(entry)

        return opt

    def _gen_request_url(self):
        workflow_id = self.valves.DIFY_WORKFLOW_ID_1  # HACK
        return "{}/workflows/{}/run".format(self.base_url, workflow_id)

    def _gen_headers(self):
        api_key = self.valves.DIFY_API_KEY_1  # HACK
        return {
            "Authorization": "Bearer {}".format(api_key),
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
