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

    def test3(_, model_skip_cf2):
        opt = model_skip_cf2.name

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
        patch_and_result_wf1,
        patch_target,
        info_endpoint,
    ):
        config = config_wf1.copy()
        mock_resp, assert_kwargs = patch_and_result_wf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Workflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    def test2(
        _,
        base_url,
        config_cf1,
        patch_and_result_cf1,
        patch_target,
        info_endpoint,
    ):
        config = config_cf1.copy()
        mock_resp, assert_kwargs = patch_and_result_cf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            model = OWUModel(base_url, config)

            opt = model.name
            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Chatflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)


class TestModelId:  ############################################################

    def test1(_, base_url, config_wf1, patch_target, info_endpoint):
        config = config_wf1.copy()
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

    def test2(_, base_url, config_cf1, patch_target, info_endpoint):
        config = config_cf1.copy()
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
