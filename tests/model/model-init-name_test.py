"""
model-init-name_test.py

Unit Tests (using pytest) for: OWUModel

- .name
- _get_app_type_and_name_by_dify_get_info()
"""

from unittest.mock import patch, Mock
import requests


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

import pytest


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def wf_provided_model1(base_url, workflow_config1):
    config = workflow_config1.copy()
    config["name"] = "My Workflow Name"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def cf_provided_model1(base_url, chatflow_config1):
    config = chatflow_config1.copy()
    config["name"] = "Example Chatflow Model/App"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture(scope="session")
def cf_no_name_model1(base_url, chatflow_config1):
    config = chatflow_config1.copy()
    del config["name"]
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


# provided
class TestProvided:  ###########################################################

    def test1(_, wf_provided_model1):
        opt = wf_provided_model1.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "My Workflow Name"

    def test2(_, cf_provided_model1):
        opt = cf_provided_model1.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Example Chatflow Model/App"

    def test3(_, cf_model_skip2):
        opt = cf_model_skip2.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Aux Example Chatflow Model/App"

    # err handling  ------------------------------------------------------------

    def test_empty_name(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["name"] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'name'"

    def test_bad_type(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["name"] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "entry in APP_MODEL_CONFIGS, value of 'name' must be str or None"
        )


class TestResponse:  ###########################################################

    def test1(_, base_url, workflow_config1):
        config = workflow_config1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "workflow",
            "name": "My Workflow App",
        }

        with patch(
            "dify_open_webui_adapter.requests.get", return_value=mock_resp
        ) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Workflow App"

            mock_get.assert_called_once_with(
                "https://api.dify.ai/v1/info",
                headers={
                    "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

    def test2(_, base_url, chatflow_config1):
        config = chatflow_config1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "advanced-chat",
            "name": "My Chatflow App",
        }

        with patch(
            "dify_open_webui_adapter.requests.get", return_value=mock_resp
        ) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Chatflow App"

            mock_get.assert_called_once_with(
                "https://api.dify.ai/v1/info",
                headers={
                    "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

    # err handling  ============================================================

    def test_bad_conncetion(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        with patch(
            "dify_open_webui_adapter.requests.get",
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            with pytest.raises(ConnectionError) as exec_info:
                OWUModel(base_url, config)
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"


# model id  ####################################################################

# TODO TODO
