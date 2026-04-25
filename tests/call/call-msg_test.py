"""
call-msg_test.py

Unit Tests (using pytest) for:

PipeCall.message
"""

import pytest

from dify_open_webui_adapter import PipeCall

# Pytest unit tests  ###########################################################


class TestGet:

    def test1(_, pipe_call_args):
        args = pipe_call_args

        call = PipeCall(**args)

        opt = call.message
        assert opt == "Hello Dify"

    def test2(_, pipe_call_args):
        args = pipe_call_args
        args["body"]["messages"] = [
            {"role": "user", "content": "FIRST USER MESSAGE"},
            {"role": "assistant", "content": "FIRST BOT REPLY"},
            {"role": "user", "content": "SECOND USER MESSAGE"},
            {"role": "assistant", "content": "SECOND BOT REPLY"},
            {"role": "user", "content": "THIRD USER MESSAGE"},
        ]

        call = PipeCall(**args)

        opt = call.message
        assert opt == "THIRD USER MESSAGE"

    # err handling  ============================================================

    def test_no_user1(_, pipe_call_args):
        args = pipe_call_args
        args["body"]["messages"] = []

        with pytest.raises(ValueError) as exec_info:
            PipeCall(**args)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("body", "messages")
        assert (
            opt[0]["msg"]
            == "List should have at least 1 item after validation, not 0"
        )
