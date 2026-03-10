"""
app-get_test.py

Unit Tests (using pytest) for:

BaseDifyApp.get_app_type_and_name()
"""

from unittest.mock import Mock, patch
import requests

import pytest


from dify_open_webui_adapter import BaseDifyApp, DifyAppType

# pytest fixtures  #############################################################

# pytest  ######################################################################


class TestGet:

    def test_wf(
        _,
        base_url,
        config_wf1,
        patch_and_result_wf1,
        patch_target,
        info_endpoint,
    ):
        config = config_wf1
        key = config["key"]
        mock_resp, assert_kwargs = patch_and_result_wf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            opt = BaseDifyApp.get_app_type_and_name(base_url, key)

            print(opt)
            app_type, response_name = opt

            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.WORKFLOW

            assert isinstance(response_name, str)
            assert response_name == "My Workflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    def test_cf(
        _,
        base_url,
        config_cf1,
        patch_and_result_cf1,
        patch_target,
        info_endpoint,
    ):
        config = config_cf1
        key = config["key"]
        mock_resp, assert_kwargs = patch_and_result_cf1

        with patch(patch_target, return_value=mock_resp) as mock_get:
            opt = BaseDifyApp.get_app_type_and_name(base_url, key)

            print(opt)
            app_type, response_name = opt

            print(app_type)
            assert isinstance(app_type, DifyAppType)
            assert app_type is DifyAppType.CHATFLOW

            assert isinstance(response_name, str)
            assert response_name == "My Chatflow App"

            mock_get.assert_called_once_with(info_endpoint, **assert_kwargs)

    # err handling  ============================================================

    def test_no_type(_, base_url, config_wf1, patch_target):
        config = config_wf1
        key = config["key"]
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "name": "Some Names",
        }

        with patch(patch_target, return_value=mock_resp):
            with pytest.raises(ValueError) as exec_info:
                BaseDifyApp.get_app_type_and_name(base_url, key)
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail to get App Type from Dify"

    def test_bad_conncetion(_, base_url, config_wf1, patch_target):
        config = config_wf1
        key = config["key"]

        with patch(
            patch_target,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            with pytest.raises(ConnectionError) as exec_info:
                BaseDifyApp.get_app_type_and_name(base_url, key)
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"
