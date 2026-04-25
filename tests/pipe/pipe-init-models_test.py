"""
pipe-init-models_test.py

Unit Tests (using pytest) for:

Pipe.__init__() populating .models
"""

# Pytest unit tests  ###########################################################


from dify_open_webui_adapter import AppModelConfig, ChatflowApp, WorkflowApp


class TestKeys:  # =============================================================

    def test_wf1(_, pipe_obj, model_id_wf1):
        key = model_id_wf1
        opt = pipe_obj.models

        print(opt)
        assert key in opt

    def test_cf1(_, pipe_obj, model_id_cf1):
        key = model_id_cf1
        opt = pipe_obj.models

        print(opt)
        assert key in opt

    def test_cf2(_, pipe_obj, model_id_cf2):
        key = model_id_cf2
        opt = pipe_obj.models

        print(opt)
        assert key in opt


class TestWf1:  # ==============================================================

    def test_config(_, pipe_obj, model_id_wf1, config_wf1):
        model = pipe_obj.models[model_id_wf1]
        config = config_wf1

        assert isinstance(model.config, AppModelConfig)
        assert model.config == config

    def test_app(_, pipe_obj, model_id_wf1):
        model = pipe_obj.models[model_id_wf1]
        app = pipe_obj.apps[model_id_wf1]

        assert isinstance(model.app, WorkflowApp)
        assert model.app is app

    def test_call(_, pipe_obj, model_id_wf1):
        model = pipe_obj.models[model_id_wf1]
        assert model.call is None


class TestCf1:  # ==============================================================

    def test_config(_, pipe_obj, model_id_cf1, config_cf1):
        model = pipe_obj.models[model_id_cf1]
        config = config_cf1

        assert isinstance(model.config, AppModelConfig)
        assert model.config == config

    def test_app(_, pipe_obj, model_id_cf1):
        model = pipe_obj.models[model_id_cf1]
        app = pipe_obj.apps[model_id_cf1]

        assert isinstance(model.app, ChatflowApp)
        assert model.app is app

    def test_call(_, pipe_obj, model_id_cf1):
        model = pipe_obj.models[model_id_cf1]
        assert model.call is None


class TestCf2:  # ==============================================================

    def test_config(_, pipe_obj, model_id_cf2, config_cf2):
        model = pipe_obj.models[model_id_cf2]
        config = config_cf2

        assert isinstance(model.config, AppModelConfig)
        assert model.config == config

    def test_app(_, pipe_obj, model_id_cf2):
        model = pipe_obj.models[model_id_cf2]
        app = pipe_obj.apps[model_id_cf2]

        assert isinstance(model.app, ChatflowApp)
        assert model.app is app

    def test_call(_, pipe_obj, model_id_cf2):
        model = pipe_obj.models[model_id_cf2]
        assert model.call is None
