"""
base_container_test.py

Unit Tests (using pytest) for: BaseContainer
"""

import pytest

from tests import EXAMPLE_CONFIGS, EXAMPLE_BODY1, EXAMPLE_BODY2

from dify_open_webui_adapter import Pipe


class TestRetrieve:  # test ._retrieve_newest_user_message()  ##################

    def test1(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model"]
        body = EXAMPLE_BODY1

        opt = chatflow._retrieve_newest_user_message(body)

        print(opt)

        assert isinstance(opt, str)
        assert opt == "FIRST USER MESSAGE"

    def test2(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model"]
        body = EXAMPLE_BODY2

        opt = chatflow._retrieve_newest_user_message(body)

        print(opt)

        assert isinstance(opt, str)
        assert opt == "THIRD USER MESSAGE"

    # err handle  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def test_no_msg(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model"]

        bad_body = {
            "stream": True,
            "model": "dify_open_webui_adapter.example-chatflow-model",
        }

        with pytest.raises(KeyError) as exec_info:
            chatflow._retrieve_newest_user_message(bad_body)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "'messages'"

    def test_no_user_msg(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model"]

        bad_body = {
            "stream": True,
            "model": "dify_open_webui_adapter.example-chatflow-model",
            "messages": [
                {"role": "assistant", "content": "FIRST BOT REPLY"},
            ],
        }

        with pytest.raises(ValueError) as exec_info:
            chatflow._retrieve_newest_user_message(bad_body)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "fail to find any 'user' messages"


class TestGenHeader:  # test ._gen_html_headers()  #############################

    def test1(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model"]

        opt = chatflow._gen_html_header()

        print(opt)

        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer u0caCsmD",
            "Content-Type": "application/json",
        }

    def test2(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-workflow-model"]

        opt = chatflow._gen_html_header()

        print(opt)

        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer eaJxetwz",
            "Content-Type": "application/json",
        }

    def test3(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        chatflow = pipe.model_containers["example-chatflow-model-2"]

        opt = chatflow._gen_html_header()

        print(opt)

        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer YIFpPns6",
            "Content-Type": "application/json",
        }
