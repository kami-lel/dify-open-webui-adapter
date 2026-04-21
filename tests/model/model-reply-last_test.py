"""
model-reply-last_test.py

Unit Tests (using pytest) for:


OWUModel._get_last_user_msg_content()
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture
def pipe_body2():
    return {
        "stream": False,
        "model": "dify_open_webui_adapter.example-chatflow-model",
        "messages": [
            {"role": "user", "content": "FIRST USER MESSAGE"},
            {"role": "assistant", "content": "FIRST BOT REPLY"},
            {"role": "user", "content": "SECOND USER MESSAGE"},
            {"role": "assistant", "content": "SECOND BOT REPLY"},
            {"role": "user", "content": "THIRD USER MESSAGE"},
        ],
    }


# Pytest unit tests  ###########################################################
class TestGet:

    def test1(_, model_wf_skip1, pipe_body1):
        model = model_wf_skip1
        body = pipe_body1

        opt = model._get_last_user_msg_content(body)
        print(opt)
        assert opt == "FIRST USER MESSAGE"

    def test2(_, model_cf_skip1, pipe_body2):
        model = model_cf_skip1
        body = pipe_body2

        opt = model._get_last_user_msg_content(body)
        print(opt)
        assert opt == "THIRD USER MESSAGE"

    # err handling  ============================================================

    def test_no_user1(_, model_wf_skip1, pipe_body1):
        model = model_wf_skip1
        body = pipe_body1
        body["messages"] = []

        with pytest.raises(ValueError) as exec_info:
            model._get_last_user_msg_content(body)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "missing user message in body"
