"""
app-base_create_app_test.py

Unit Tests (using pytest) for:

BaseDifyApp.create_app()
"""

import requests
from unittest.mock import patch, Mock


import pytest


from dify_open_webui_adapter import BaseDifyApp, WorkflowApp, ChatflowApp

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_wf1(config_wf1, patch_target_get, mock_info_wf):
    config = config_wf1
    mock = mock_info_wf

    with patch(patch_target_get, return_value=mock) as mock_get:
        app = BaseDifyApp.create_app(config)

    return app, mock_get


@pytest.fixture(scope="class")
def testee_cf1(config_cf1, patch_target_get, mock_info_cf):
    config = config_cf1
    mock = mock_info_cf

    with patch(patch_target_get, return_value=mock) as mock_get:
        app = BaseDifyApp.create_app(config)

    return app, mock_get


# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_type(_, testee_wf1):
        app, _ = testee_wf1
        assert isinstance(app, WorkflowApp)

    def test_config(_, testee_wf1, config_wf1):
        app, _ = testee_wf1

        opt = app.config
        print(opt)
        assert opt is config_wf1

    def test_model(_, testee_wf1):
        app, _ = testee_wf1
        assert app.model is None

    def test_name(_, testee_wf1, app_response_name_wf1):
        app, _ = testee_wf1
        opt = app.response_name
        print(opt)
        assert opt == app_response_name_wf1

    def test_assert(_, testee_wf1, mock_assertee_info_wf):
        _, mock_get = testee_wf1
        args, kwargs = mock_assertee_info_wf

        mock_get.assert_called_once_with(*args, **kwargs)


class TestCf1:  # ==============================================================

    def test_type(_, testee_cf1):
        app, _ = testee_cf1
        assert isinstance(app, ChatflowApp)

    def test_config(_, testee_cf1, config_cf1):
        app, _ = testee_cf1

        opt = app.config
        print(opt)
        assert opt is config_cf1

    def test_model(_, testee_cf1):
        app, _ = testee_cf1
        assert app.model is None

    def test_name(_, testee_cf1, app_response_name_cf1):
        app, _ = testee_cf1

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_cf1

    def test_assert(_, testee_cf1, mock_assertee_info_cf):
        _, mock_get = testee_cf1
        args, kwargs = mock_assertee_info_cf

        mock_get.assert_called_once_with(*args, **kwargs)


class TestErr:  # ==============================================================

    def test_no_type(_, config_wf1, patch_target_get):
        config = config_wf1
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "name": "Some Names",
        }

        with patch(patch_target_get, return_value=mock_resp):
            with pytest.raises(ValueError) as exec_info:
                BaseDifyApp.create_app(config)
            opt = exec_info.value.args[0]

            print(opt)
            assert (
                opt
                == "missing App Type ('mode') from Dify: {'name': 'Some Names'}"
            )

    def test_bad_connections(_, config_wf1, patch_target_get):
        config = config_wf1

        with patch(
            patch_target_get,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            with pytest.raises(ConnectionError) as exec_info:
                BaseDifyApp.create_app(config)
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail to connect Dify: Bad Connection"
