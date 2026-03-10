"""
app-base-init_test.py

Unit Tests (using pytest) for:

BaseDifyApp.__init__()
"""

import pytest

from dify_open_webui_adapter import WorkflowApp

# pytest  ######################################################################


class TestWf1:  # ==============================================================

    def test_model(_, app_skip_wf1, model_skip_wf1):
        app = app_skip_wf1
        model = model_skip_wf1

        assert app.model is model

    def test_base_url(_, app_skip_wf1, base_url):
        app = app_skip_wf1

        opt = app.base_url
        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test_key(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "068937402cc741689986cc5b6ed433a"

    def test_disallows(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt

    def test_msg(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.current_user_msg_content

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_enables(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.current_enable_stream

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


class TestLocalWf1:  # =========================================================

    def test_model(_, app_wf_alt_url, model_wf_alt_url):
        app = app_wf_alt_url
        model = model_wf_alt_url

        assert app.model is model

    def test_base_url(_, app_wf_alt_url, base_url_alt):
        app = app_wf_alt_url

        opt = app.base_url
        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url_alt

    def test_key(_, app_wf_alt_url):
        app = app_wf_alt_url
        opt = app.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "068937402cc741689986cc5b6ed433a"

    def test_disallows(_, app_wf_alt_url):
        app = app_wf_alt_url
        opt = app.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt

    def test_msg(_, app_wf_alt_url):
        app = app_wf_alt_url
        opt = app.current_user_msg_content

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_enables(_, app_wf_alt_url):
        app = app_wf_alt_url
        opt = app.current_enable_stream

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


class TestCf1:  # ==============================================================

    def test_model(_, app_skip_cf1, model_skip_cf1):
        app = app_skip_cf1
        model = model_skip_cf1
        assert app.model is model

    def test_base_url(_, app_skip_cf1, base_url):
        app = app_skip_cf1

        opt = app.base_url
        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test_key(_, app_skip_cf1):
        app = app_skip_cf1
        opt = app.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "f2277b0e16154cba981c866bdc124386"

    def test_disallows(_, app_skip_cf1):
        app = app_skip_cf1
        opt = app.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt

    def test_msg(_, app_skip_cf1):
        app = app_skip_cf1
        opt = app.current_user_msg_content

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_enables(_, app_skip_cf1):
        app = app_skip_cf1
        opt = app.current_enable_stream

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


class TestErr:  #  =============================================================
    def test_disallow_type(_, base_url, config_wf1):
        config = config_wf1.copy()

        config["disallows_streaming"] = 123

        with pytest.raises(TypeError) as exec_info:
            WorkflowApp(None, base_url, config)
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "entry in APP_MODEL_CONFIGS, value of 'disallows_streaming' "
            "must be bool: 123"
        )
