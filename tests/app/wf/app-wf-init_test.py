"""
app-wf-init_test.py

Unit Tests (using pytest) for:

- WorkflowApp.__init__()
"""

# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_config(_, app_direct_wf1, config_wf1):
        app = app_direct_wf1

        opt = app.config
        print(opt)
        assert opt is config_wf1

    def test_model(_, app_direct_wf1):
        app = app_direct_wf1
        assert app.model is None

    def test_name(_, app_direct_wf1, app_response_name_wf1):
        app = app_direct_wf1

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_wf1
