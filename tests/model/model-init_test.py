"""
model-init_test.py

Unit Tests (using pytest) for:

OWUModel.__init__()
"""

import pytest


from dify_open_webui_adapter import (
    OWUModel,
    AppModelConfig,
    WorkflowApp,
    ChatflowApp,
)

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def local_model_wf(config_wf1, app_direct_wf1):
    config = config_wf1
    app = app_direct_wf1
    return OWUModel(config, app)


@pytest.fixture(scope="class")
def local_model_cf(config_cf1, app_direct_cf1):
    config = config_cf1
    app = app_direct_cf1
    return OWUModel(config, app)


# Pytest unit tests  ###########################################################


class TestWf:  # ===============================================================

    def test_config(_, local_model_wf, config_wf1):
        model = local_model_wf
        config = config_wf1

        assert isinstance(model.config, AppModelConfig)
        assert model.config is config

    def test_app(_, local_model_wf, app_direct_wf1):
        model = local_model_wf
        app = app_direct_wf1

        assert isinstance(model.app, WorkflowApp)
        assert model.app is app

    def test_call(_, local_model_wf):
        model = local_model_wf
        assert model.call is None


class TestCf:  # ===============================================================

    def test_config(_, local_model_cf, config_cf1):
        model = local_model_cf
        config = config_cf1

        assert isinstance(model.config, AppModelConfig)
        assert model.config is config

    def test_app(_, local_model_cf, app_direct_cf1):
        model = local_model_cf
        app = app_direct_cf1

        assert isinstance(model.app, ChatflowApp)
        assert model.app is app

    def test_call(_, local_model_cf):
        model = local_model_cf
        assert model.call is None
