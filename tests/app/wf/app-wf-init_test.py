"""
app-wf-init_test.py

Unit Tests (using pytest) for:

- WorkflowApp.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


@pytest.fixture
def local_model1(base_url, workflow_config1):
    config = workflow_config1.copy()
    config["query_input_field_identifier"] = "aaaaaa"
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )
    return model


@pytest.fixture
def local_app1(local_model1):
    return local_model1.app


@pytest.fixture
def local_model2(base_url, workflow_config1):
    config = workflow_config1.copy()
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


@pytest.fixture
def local_app2(local_model2):
    return local_model2.app


# tests  #######################################################################


class Test1:  # ================================================================

    def test_model(_, wf_app1, wf_model1):
        app = wf_app1
        model = wf_model1
        assert app.model is model

    def test_query(_, wf_app1):
        opt = wf_app1.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "query"

    def test_repply(_, wf_app1):
        opt = wf_app1.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "answer"

    def test_fields(_, wf_app1):
        opt = wf_app1.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}


class TestL1:  # ===============================================================

    def test_model(_, local_app1, local_model1):
        app = local_app1
        model = local_model1
        assert app.model is model

    def test_query(_, local_app1):
        opt = local_app1.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "aaaaaa"

    def test_repply(_, local_app1):
        opt = local_app1.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "answer"

    def test_fields(_, local_app1):
        opt = local_app1.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}


class TestL2:  # ===============================================================

    def test_model(_, local_app2, local_model2):
        app = local_app2
        model = local_model2
        assert app.model is model

    def test_query(_, local_app2):
        opt = local_app2.query_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "query"

    def test_repply(_, local_app2):
        opt = local_app2.reply_identifier

        print(opt)
        assert isinstance(opt, str)
        assert opt == "zzzzzz"

    def test_fields(_, local_app2):
        opt = local_app2.input_fields

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {"foo": "aabbcc", "bar": 123}
