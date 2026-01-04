"""
workflow_container_test.py

Unit Tests (using pytest) for: WorkflowContainers
"""

import pytest

from tests import EXAMPLE_CONFIGS, EXAMPLE_BODY1, EXAMPLE_BODY2

from dify_open_webui_adapter import Pipe


class TestGenRequestURL:  # test ._gen_request_url()  ##########################

    def test1(_):
        base_url = "https://api.dify.ai/v1"
        pipe = Pipe(
            app_model_configs=EXAMPLE_CONFIGS, base_url_override=base_url
        )
        chatflow = pipe.containers["example-workflow-model"]

        opt = chatflow._gen_request_url()

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://api.dify.ai/v1/workflows/run"

    def test2(_):
        base_url = "http://11.22.33.44:1234/v1"
        pipe = Pipe(
            app_model_configs=EXAMPLE_CONFIGS, base_url_override=base_url
        )
        chatflow = pipe.containers["example-workflow-model"]

        opt = chatflow._gen_request_url()

        print(opt)
        assert isinstance(opt, str)
        assert opt == "http://11.22.33.44:1234/v1/workflows/run"


class TestPayload:  # test ._build_html_payloads()  ############################
    pass  # TODO


class TestExtractResponse:  # test ._extract_dify_response()  ##################
    pass  # TODO
