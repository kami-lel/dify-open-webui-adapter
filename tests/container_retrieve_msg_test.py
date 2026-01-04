"""
container_retrieve_msg_test.py

Unit Tests (using pytest) for:

- BaseContainer._retrieve_newest_user_message()
"""

import pytest

from tests import EXAMPLE_CONFIGS, EXAMPLE_BODY1, EXAMPLE_BODY2

from dify_open_webui_adapter import Pipe


class TestRetrieve:

    def test1(_):
        pipe = Pipe(app_model_configs=EXAMPLE_CONFIGS)
        chatflow = pipe.containers["example-chatflow-model"]
        body = EXAMPLE_BODY1

        opt = chatflow._retrieve_newest_user_message(body)

        print(opt)

        assert isinstance(opt, str)
        assert opt == "FIRST USER MESSAGE"

    def test2(_):
        pipe = Pipe(app_model_configs=EXAMPLE_CONFIGS)
        chatflow = pipe.containers["example-chatflow-model"]
        body = EXAMPLE_BODY2

        opt = chatflow._retrieve_newest_user_message(body)

        print(opt)

        assert isinstance(opt, str)
        assert opt == "THIRD USER MESSAGE"


# err handle  ################################################################## TODO


class TestBadBody:

    def test_no_msg(_):
        pipe = Pipe(app_model_configs=EXAMPLE_CONFIGS)
        chatflow = pipe.containers["example-chatflow-model"]

        bad_body = {
            "stream": True,
            "model": "dify_open_webui_adapter.example-chatflow-model",
        }

        with pytest.raises(ValueError) as exec_info:
            chatflow._retrieve_newest_user_message(bad_body)

        opt = str(exec_info.value)
        print(opt)

        assert opt == ""
