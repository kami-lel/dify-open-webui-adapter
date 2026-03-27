"""
model-init-name_test.py

Unit Tests (using pytest) for: OWUModel

- .name
"""

from unittest.mock import patch, Mock


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

import pytest


# provided
class TestProvided:  ###########################################################

    def test1(_, model_wf_provide_name):
        opt = model_wf_provide_name.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "My Workflow Name"

    def test2(_, model_cf_provide_name):
        opt = model_cf_provide_name.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Example Chatflow Model/App"

    def test3(_, model_cf_skip2):
        opt = model_cf_skip2.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Aux Example Chatflow Model/App"

    # err handling  ------------------------------------------------------------

    def test_empty_name(_, base_url, config_wf1):
        config = config_wf1.copy()

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

    def test_bad_type(_, base_url, config_wf1):
        config = config_wf1.copy()

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
        config_wf1,
        mock_info_wf,
        assertee_info_wf,
        patch_target_get,
    ):
        config = config_wf1.copy()
        mock_resp = mock_info_wf

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Workflow App"

            mock_get.assert_called_once_with(
                *(assertee_info_wf[0]), **(assertee_info_wf[1])
            )

    def test2(
        _,
        base_url,
        config_cf1,
        mock_info_cf,
        assertee_info_cf,
        patch_target_get,
    ):
        config = config_cf1.copy()
        mock_resp = mock_info_cf

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Chatflow App"

            mock_get.assert_called_once_with(
                *(assertee_info_cf[0]), **(assertee_info_cf[1])
            )


class TestModelId:  ############################################################

    def test1(
        _,
        base_url,
        config_wf1,
        patch_target_get,
        endpoint_info,
        authorization_wf1,
    ):
        config = config_wf1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "workflow",
        }

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "example-workflow-model"

            mock_get.assert_called_once_with(
                endpoint_info,
                headers={
                    "Authorization": authorization_wf1,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

    def test2(
        _,
        base_url,
        config_cf1,
        patch_target_get,
        endpoint_info,
        authorization_cf1,
    ):
        config = config_cf1.copy()
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "advanced-chat",
        }

        with patch(patch_target_get, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "example-chatflow-model"

            mock_get.assert_called_once_with(
                endpoint_info,
                headers={
                    "Authorization": authorization_cf1,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )
