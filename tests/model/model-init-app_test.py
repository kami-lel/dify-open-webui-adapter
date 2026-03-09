"""
model-init-app_test.py

Unit Tests (using pytest) for OWUModel:

- .app_type
- .app
"""

from unittest.mock import patch, Mock


import pytest


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
    WorkflowApp,
    ChatflowApp,
)


class TestApp:

    def test_cf(
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

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.CHATFLOW

            app = model.app
            print(app)
            assert isinstance(app, ChatflowApp)

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    def test_wf(
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

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.WORKFLOW

            app = model.app
            print(app)
            assert isinstance(app, WorkflowApp)

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    # err handling  ------------------------------------------------------------

    def test_no_type(_, base_url, workflow_config1, patch_target):
        config = workflow_config1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "name": "Some Names",
        }

        with patch(patch_target, return_value=mock_resp):
            with pytest.raises(ValueError) as exec_info:
                OWUModel(base_url, config)
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail to get App Type from Dify"
