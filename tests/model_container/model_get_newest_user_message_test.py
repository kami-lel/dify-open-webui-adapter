"""
model_reply_test.py

Unit Tests (using pytest) for: OWUModel._get_newest_user_message_from_body()
"""

import pytest

from dify_open_webui_adapter import OWUModel

from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_BODY1,
    EXAMPLE_BODY2,
)


class TestBody:
    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model._get_newest_user_message_from_body(EXAMPLE_BODY1)

        print(opt)
        assert isinstance(opt, str)
        assert opt == "FIRST USER MESSAGE"

    def test2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model._get_newest_user_message_from_body(EXAMPLE_BODY2)

        print(opt)
        assert isinstance(opt, str)
        assert opt == "THIRD USER MESSAGE"


class TestNoMessage:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )
        body = EXAMPLE_BODY1.copy()
        body["messages"] = []

        with pytest.raises(ValueError) as exec_info:
            model._get_newest_user_message_from_body(body)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "fail to find any 'user' messages"
