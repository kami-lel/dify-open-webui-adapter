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

    def test1(_, wf_provide_name_model1):
        opt = wf_provide_name_model1.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "My Workflow Name"

    def test2(_, cf_provide_name_model1):
        opt = cf_provide_name_model1.name

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

    def test1(
        _,
        base_url,
        workflow_config1,
        patch_and_result_cf1,
        patch_target,
        info_endpoint,
    ):
        config = workflow_config1.copy()
        mock_resp, assert_kwargs = patch_and_result_cf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Chatflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    def test2(
        _,
        base_url,
        chatflow_config1,
        patch_and_result_wf1,
        patch_target,
        info_endpoint,
    ):
        config = chatflow_config1.copy()
        mock_resp, assert_kwargs = patch_and_result_wf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Workflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)


class TestModelId:  ############################################################

    def test1(_, base_url, workflow_config1, patch_target, info_endpoint):
        config = workflow_config1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "workflow",
        }

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "example-workflow-model"

            mock_get.assert_called_once_with(
                info_endpoint,
                headers={
                    "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

    def test2(_, base_url, chatflow_config1, patch_target, info_endpoint):
        config = chatflow_config1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "advanced-chat",
        }

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "example-chatflow-model"

            mock_get.assert_called_once_with(
                info_endpoint,
                headers={
                    "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
                    "Content-Type": "application/json",
                },
                timeout=30,
            )
