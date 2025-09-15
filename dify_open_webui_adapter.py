# todo docstring for this script

import json

from pydantic import BaseModel, Field
import requests

__version__ = "1.0.0-alpha"
__author__ = "kamiLeL"


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

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body):
        self.base_url = self.valves.DIFY_BACKEND_API_BASE_URL
        self.api_key = self.valves.DIFY_API_KEY
        self.workflow_id = self.valves.DIFY_WORKFLOW_ID

        # get user's input
        message = body["messages"][0]["content"]

        # send request to Dify
        # FIXME use try to catch request error

        response = requests.post(
            self._gen_request_url(),
            headers=self._gen_headers(),
            data=self._build_payload(message),
            timeout=REQUEST_TIMEOUT,
        )

        # parse returned data
        # FIXME error handling for non-200 response
        content = response.json()
        output = content["data"]["outputs"]["output"]
        return output

    def _gen_request_url(self):
        return "{}/workflows/{}/run".format(self.base_url, self.workflow_id)

    def _gen_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.api_key),
            "Content-Type": "application/json",
        }

    def _build_payload(self, message):
        payload_dict = {
            "inputs": {"input": message},
            "response_mode": "blocking",
            "user": "user",
        }
        return json.dumps(payload_dict)
