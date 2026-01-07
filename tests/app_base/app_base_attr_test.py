"""
app_base_attr_test.py

tests for: BaseDifyApp

- .model
- .base_url
- .model_id
- .http_header
"""

from dify_open_webui_adapter import OWUModel

from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_WORKFLOW_CONFIG,
    EXAMPLE_CHATFLOW_CONFIG,
)


class Test:

    def test_case1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        app = model.app

        print(app)
        assert app.model is model
        assert app.base_url == EXAMPLE_BASE_URL
        assert app.model_id == "example-workflow-model"
        assert app.http_header(False) == model.http_header(False)

    def test_case2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        app = model.app

        print(app)
        assert app.model is model
        assert app.base_url == EXAMPLE_BASE_URL
        assert app.model_id == "example-chatflow-model"
        assert app.http_header(True) == model.http_header(True)
