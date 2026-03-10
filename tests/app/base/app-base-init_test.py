"""
app-base-init_test.py

Unit Tests (using pytest) for:

BaseDifyApp.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def model_local_wf1(base_url_alt, config_wf1):
    return OWUModel(
        base_url_alt,
        config_wf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def app_local_wf1(model_local_wf1):
    return model_local_wf1.app


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


class TestLocalWf1:  # =========================================================

    def test_model(_, app_local_wf1, model_local_wf1):
        app = app_local_wf1
        model = model_local_wf1

        assert app.model is model

    def test_base_url(_, app_local_wf1, base_url_alt):
        app = app_local_wf1

        opt = app.base_url
        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url_alt

    def test_key(_, app_local_wf1):
        app = app_local_wf1
        opt = app.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "068937402cc741689986cc5b6ed433a"

    def test_disallows(_, app_local_wf1):
        app = app_local_wf1
        opt = app.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


# TODO local one, alt url


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


class TestErr:  #  =============================================================

    def test1(_):
        pass  # TODO
