"""
app-cf-init_test.py

Unit Tests (using pytest) for:

- ChatflowApp.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


@pytest.fixture
def local_model1(base_url, chatflow_config1):
    config = chatflow_config1
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )
    return model


@pytest.fixture
def local_app1(local_model1):
    return local_model1.app


# tests  #######################################################################


class Test1:  # ================================================================

    def test_model(_, cf_app1, cf_model1):
        app = cf_app1
        model = cf_model1
        assert app.model is model

    def test_chat_id(_, cf_app1):
        opt = cf_app1.current_chat_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_ids(_, cf_app1):
        opt = cf_app1.chat2conversation_ids

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}


class TestL1:  # ===============================================================

    def test_model(_, local_app1, local_model1):
        app = local_app1
        model = local_model1
        assert app.model is model

    def test_chat_id(_, local_app1):
        opt = local_app1.current_chat_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_ids(_, local_app1):
        opt = local_app1.chat2conversation_ids

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}
