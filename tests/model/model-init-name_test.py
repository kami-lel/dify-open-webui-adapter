"""
model-init-name_test.py

Unit Tests (using pytest) for:

setting .display_name during OWUModel.__init__()
"""

from dify_open_webui_adapter import OWUModel

# Pytest unit tests  ###########################################################


class TestName:

    def test1(_, config_wf1, app_direct_wf1, app_given_name_wf1):
        config = config_wf1
        app = app_direct_wf1

        model = OWUModel(config, app)

        opt = model.display_name
        print(opt)

        assert isinstance(opt, str)
        assert opt == app_given_name_wf1

    def test2(_, config_cf2, app_direct_cf1, app_response_name_cf1):
        config = config_cf2
        app = app_direct_cf1

        model = OWUModel(config, app)

        opt = model.display_name
        print(opt)

        assert isinstance(opt, str)
        assert opt == app_response_name_cf1

    def test3(_, config_cf2, app_direct_cf2):
        config = config_cf2
        app = app_direct_cf2

        model = OWUModel(config, app)

        opt = model.display_name
        print(opt)

        assert isinstance(opt, str)
        assert opt == "example-chatflow-model-2"
