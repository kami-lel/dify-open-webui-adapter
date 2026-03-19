"""
model-init-app_test.py

Unit Tests (using pytest) for OWUModel:

- .app_type
- .app
"""

from unittest.mock import patch


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
    WorkflowApp,
    ChatflowApp,
)


class TestApp:

    def test_wf(
        _,
        base_url,
        config_wf1,
        patch_and_result_wf1,
        patch_target_get,
        info_endpoint,
    ):
        config = config_wf1
        mock_resp, assert_kwargs = patch_and_result_wf1

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.WORKFLOW

            app = model.app
            print(app)
            assert isinstance(app, WorkflowApp)

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    def test_cf(
        _,
        base_url,
        config_cf1,
        patch_and_result_cf1,
        patch_target_get,
        info_endpoint,
    ):
        config = config_cf1
        mock_resp, assert_kwargs = patch_and_result_cf1

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.CHATFLOW

            app = model.app
            print(app)
            assert isinstance(app, ChatflowApp)

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)
