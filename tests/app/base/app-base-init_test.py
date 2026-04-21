"""
app-base-init_test.py

Unit Tests (using pytest) for:

BaseDifyApp.__init__()
"""

import pytest

from dify_open_webui_adapter import WorkflowApp, ChatflowApp


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def local_app_wf1(config_wf1, info_response_wf1):
    return WorkflowApp(config_wf1, info_response_wf1)


@pytest.fixture(scope="class")
def local_app_cf1(config_cf1, info_response_cf1):
    return ChatflowApp(config_cf1, info_response_cf1)


@pytest.fixture(scope="class")
def local_app_cf2(config_cf2):
    return ChatflowApp(config_cf2, {})


# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_config(_, local_app_wf1, config_wf1):
        app = local_app_wf1

        opt = app.config
        print(opt)
        assert opt is config_wf1

    def test_model(_, local_app_wf1):
        app = local_app_wf1
        assert app.model is None

    def test_name(_, local_app_wf1, app_response_name_wf1):
        app = local_app_wf1

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_wf1


class TestCf1:  # ==============================================================

    def test_config(_, local_app_cf1, config_cf1):
        app = local_app_cf1

        opt = app.config
        print(opt)
        assert opt is config_cf1

    def test_model(_, local_app_cf1):
        app = local_app_cf1
        assert app.model is None

    def test_name(_, local_app_cf1, app_response_name_cf1):
        app = local_app_cf1

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_cf1


class TestCf2:  # ==============================================================

    def test_config(_, local_app_cf2, config_cf2):
        app = local_app_cf2

        opt = app.config
        print(opt)
        assert opt is config_cf2

    def test_model(_, local_app_cf2):
        app = local_app_cf2
        assert app.model is None

    def test_name(_, local_app_cf2):
        app = local_app_cf2

        opt = app.response_name
        print(opt)
        assert opt is None
