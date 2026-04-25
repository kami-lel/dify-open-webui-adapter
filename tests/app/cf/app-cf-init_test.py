"""
app-cf-init_test.py

Unit Tests (using pytest) for:

- ChatflowApp.__init__()
"""

# tests  #######################################################################


class TestCf1:  # ==============================================================

    def test_config(_, app_direct_cf1, config_cf1):
        app = app_direct_cf1

        opt = app.config
        print(opt)
        assert opt is config_cf1

    def test_model(_, app_direct_cf1):
        app = app_direct_cf1
        assert app.model is None

    def test_name(_, app_direct_cf1, app_response_name_cf1):
        app = app_direct_cf1

        opt = app.response_name
        print(opt)
        assert opt == app_response_name_cf1


class TestCf2:  # ==============================================================

    def test_config(_, app_direct_cf2, config_cf2):
        app = app_direct_cf2

        opt = app.config
        print(opt)
        assert opt is config_cf2

    def test_model(_, app_direct_cf2):
        app = app_direct_cf2
        assert app.model is None

    def test_name(_, app_direct_cf2):
        app = app_direct_cf2

        opt = app.response_name
        print(opt)
        assert opt is None
