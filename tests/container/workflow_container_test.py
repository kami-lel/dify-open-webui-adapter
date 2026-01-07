"""
workflow_container_test.py

Unit Tests (using pytest) for: WorkflowContainers
"""

import pytest

from tests import EXAMPLE_CONFIGS

from dify_open_webui_adapter import Pipe


class TestPayload:  ############################################################
    # test ._build_html_payloads()

    def test1(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-workflow-model"]
        newest_user_message = "FIRST USER MESSAGE"

        opt = chatflow._build_html_payloads(
            newest_user_message=newest_user_message
        )

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {
            "inputs": {"input": newest_user_message},
            "response_mode": "blocking",
            "user": "user",
        }


class TestExtractResponse:  ####################################################
    # test ._extract_dify_response()

    def test1(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-workflow-model"]
        response_json = {
            "data": {"outputs": {"output": "BOT RESPONSE CONTENT"}}
        }

        opt = chatflow._extract_dify_response(response_json)

        print(opt)
        assert isinstance(opt, str)
        assert opt == "BOT RESPONSE CONTENT"

    def test_bad_response1(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-workflow-model"]
        response_json = {"data": {"outputs": {}}}

        with pytest.raises(KeyError) as exec_info:
            chatflow._extract_dify_response(response_json)

        msg = exec_info.value.args[0]
        print(msg)
        assert msg == "fail to parse Dify response, missing key: output"
