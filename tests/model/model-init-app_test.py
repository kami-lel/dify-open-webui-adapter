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

# FIXME


class TestApp:

    def test_wf(
        _,
        base_url,
        config_wf1,
        mock_info_wf,
        assertee_info_wf,
        patch_target_get,
    ):
        config = config_wf1
        mock_resp = mock_info_wf

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.WORKFLOW

            app = model.app
            print(app)
            assert isinstance(app, WorkflowApp)

            mock_get.assert_called_once_with(
                *(assertee_info_wf[0]), **(assertee_info_wf[1])
            )

    def test_cf(
        _,
        base_url,
        config_cf1,
        mock_info_cf,
        assertee_info_cf,
        patch_target_get,
    ):
        config = config_cf1
        mock_resp = mock_info_cf

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            app_type = model.app_type
            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.CHATFLOW

            app = model.app
            print(app)
            assert isinstance(app, ChatflowApp)

            mock_get.assert_called_once_with(
                *(assertee_info_cf[0]), **(assertee_info_cf[1])
            )
