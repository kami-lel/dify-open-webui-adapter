"""
get_model_id_and_name_test.py

Unit Tests (using pytest) for: OWUModel.get_model_id_and_name()
"""

from dify_open_webui_adapter import OWUModel


from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_WORKFLOW_CONFIG,
)


class TestGetModelIdAndName:

    def test_provided_name1(_):
        WORKFLOW_NAME = "My Workflow Name"

        config = EXAMPLE_WORKFLOW_CONFIG.copy()
        config["name"] = WORKFLOW_NAME

        model = OWUModel(
            EXAMPLE_BASE_URL,
            config,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.get_model_id_and_name()

        print(opt)
        assert isinstance(opt, dict)
        assert "id" in opt
        assert "name" in opt

        assert all(isinstance(v, str) for v in opt.values())

        assert opt["id"] == "example-workflow-model"
        assert opt["name"] == WORKFLOW_NAME

    def test_provided_name2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.get_model_id_and_name()

        print(opt)
        assert isinstance(opt, dict)
        assert "id" in opt
        assert "name" in opt

        assert all(isinstance(v, str) for v in opt.values())

        assert opt["id"] == "example-chatflow-model"
        assert opt["name"] == "Example Chatflow Model/App"

    def test_model_id1(_):
        model = OWUModel(
            EXAMPLE_CHATFLOW_CONFIG,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.get_model_id_and_name()

        print(opt)
        assert isinstance(opt, dict)
        assert "id" in opt
        assert "name" in opt

        assert all(isinstance(v, str) for v in opt.values())

        assert opt["id"] == "example-workflow-model"
        assert opt["name"] == "example-workflow-model"

    def test_model_id2(_):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config["name"]

        model = OWUModel(
            EXAMPLE_BASE_URL,
            config,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.get_model_id_and_name()

        print(opt)
        assert isinstance(opt, dict)
        assert "id" in opt
        assert "name" in opt

        assert all(isinstance(v, str) for v in opt.values())

        assert opt["id"] == "example-chatflow-model"
        assert opt["name"] == "example-chatflow-model"
