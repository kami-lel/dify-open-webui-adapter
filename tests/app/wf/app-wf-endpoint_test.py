"""
app-wf-endpoint_test.py

Unit Tests (using pytest) for:

WorkflowApp.main_url
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


# pytest fixtures  #############################################################
@pytest.fixture
def local_app1(chatflow_config1):
    base_url = "http://11.22.33.44"
    config = chatflow_config1
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )
    return model.app


# tests  #######################################################################


class Test1:

    def test1(_, cf_app1):
        opt = cf_app1.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://api.dify.ai/v1/workflows/run"

    def test_local1(_, local_app1):
        opt = local_app1.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "http://11.22.33.44/workflows/run"
