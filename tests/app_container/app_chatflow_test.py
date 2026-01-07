"""
app_chatflow_test.py

Unit Tests (using pytest) for: ChatflowDifyApp
"""

from dify_open_webui_adapter import OWUModel, DifyAppType
from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
)


class TestEndpointUrl:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
            app_type_override=DifyAppType.CHATFLOW,
        )
        app = model.app

        opt = app.endpoint_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://api.dify.ai/v1/chat-messages"

    def test2(_):
        base_url = "http://11.22.33.44:1234/v1"
        model = OWUModel(
            base_url,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
            app_type_override=DifyAppType.CHATFLOW,
        )
        app = model.app

        opt = app.endpoint_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "http://11.22.33.44:1234/v1/chat-messages"
