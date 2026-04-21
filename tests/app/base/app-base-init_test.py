"""
app-base-init_test.py

Unit Tests (using pytest) for:

BaseDifyApp.__init__()
"""

import pytest

from dify_open_webui_adapter import WorkflowApp, ChatflowApp


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def local_app_wf1(config_wf1, app_name_wf1):
    return WorkflowApp(config_wf1, {"name": app_name_wf1})


# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_config(_, local_app_wf1, config_wf1):
        app = local_app_wf1

        opt = app.config
        print(opt)
        assert opt is config_wf1

    def test_model(_, local_app_wf1):
        app = local_app_wf1
        assert app.config is None

    def test_name(_, local_app_wf1, app_name_wf1):
        app = local_app_wf1

        opt = app.response_name
        print(opt)
        assert opt == app_name_wf1


# TODO
