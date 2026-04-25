"""
pipe-init-apps_test.py

Unit Tests (using pytest) for:

Pipe.__init__() populating .apps
"""

from dify_open_webui_adapter import ChatflowApp, WorkflowApp

# Pytest unit tests  ###########################################################


class TestKeys:  # =============================================================

    def test_wf1(_, pipe_obj, model_id_wf1):
        key = model_id_wf1
        opt = pipe_obj.apps

        print(opt)
        assert key in opt

    def test_cf1(_, pipe_obj, model_id_cf1):
        key = model_id_cf1
        opt = pipe_obj.apps

        print(opt)
        assert key in opt

    def test_cf2(_, pipe_obj, model_id_cf2):
        key = model_id_cf2
        opt = pipe_obj.apps

        print(opt)
        assert key in opt


class TestWf1:  # ==============================================================

    def test_type(_, pipe_obj, model_id_wf1):
        app = pipe_obj.apps[model_id_wf1]
        print(app)
        assert isinstance(app, WorkflowApp)

    def test_config(_, pipe_obj, model_id_wf1, config_wf1):
        app = pipe_obj.apps[model_id_wf1]

        opt = app.config
        print(opt)
        assert opt == config_wf1

    def test_model(_, pipe_obj, model_id_wf1):
        app = pipe_obj.apps[model_id_wf1]
        model = pipe_obj.models[model_id_wf1]
        assert app.model is model

    def test_name(_, pipe_obj, model_id_wf1, app_response_name_wf1):
        app = pipe_obj.apps[model_id_wf1]
        opt = app.response_name
        print(opt)
        assert opt == app_response_name_wf1


class TestCf1:  # ==============================================================

    def test_type(_, pipe_obj, model_id_cf1):
        app = pipe_obj.apps[model_id_cf1]
        assert isinstance(app, ChatflowApp)

    def test_config(_, pipe_obj, model_id_cf1, config_cf1):
        app = pipe_obj.apps[model_id_cf1]

        opt = app.config
        print(opt)
        assert opt == config_cf1

    def test_model(_, pipe_obj, model_id_cf1):
        app = pipe_obj.apps[model_id_cf1]
        model = pipe_obj.models[model_id_cf1]
        assert app.model is model

    def test_name(_, pipe_obj, model_id_cf1, app_response_name_cf1):
        app = pipe_obj.apps[model_id_cf1]

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_cf1


class TestCf2:  # ==============================================================

    def test_type(_, pipe_obj, model_id_cf2):
        app = pipe_obj.apps[model_id_cf2]
        assert isinstance(app, ChatflowApp)

    def test_config(_, pipe_obj, model_id_cf2, config_cf2):
        app = pipe_obj.apps[model_id_cf2]

        opt = app.config
        print(opt)
        assert opt == config_cf2

    def test_model(_, pipe_obj, model_id_cf2):
        app = pipe_obj.apps[model_id_cf2]
        model = pipe_obj.models[model_id_cf2]
        assert app.model is model

    def test_name(_, pipe_obj, model_id_cf2):
        app = pipe_obj.apps[model_id_cf2]

        opt = app.response_name
        print(opt)
        assert opt is None
