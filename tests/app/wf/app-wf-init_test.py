"""
app-wf-init_test.py

Unit Tests (using pytest) for:

- WorkflowApp.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


# models  ======================================================================
@pytest.fixture
def model_local2(base_url, config_wf1):
    config = config_wf1.copy()
    config["reply_output_variable_identifier"] = "zzzzzz"
    config["foo"] = "aabbcc"
    config["bar"] = 123
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )
    return model


# apps  ========================================================================


@pytest.fixture
def app_local2(model_local2):
    return model_local2.app


# tests  #######################################################################


class Test1:  # ================================================================

    def test_query(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "query"

    def test_repply(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "answer"

    def test_fields(_, app_skip_wf1):
        app = app_skip_wf1
        opt = app.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}


class TestLocal1:  # ===========================================================

    def test_query(_, app_changed_input):
        app = app_changed_input
        opt = app.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Input"

    def test_repply(_, app_changed_input):
        app = app_changed_input
        opt = app.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "answer"

    def test_fields(_, app_changed_input):
        app = app_changed_input
        opt = app.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}


class TestLocal2:  # ===========================================================

    def test_query(_, app_local2):
        app = app_local2
        opt = app.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "query"

    def test_repply(_, app_local2):
        app = app_local2
        opt = app.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "zzzzzz"

    def test_fields(_, app_local2):
        app = app_local2
        opt = app.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {"foo": "aabbcc", "bar": 123}
