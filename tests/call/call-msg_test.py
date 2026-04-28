"""
call-msg_test.py

Unit Tests (using pytest) for:

PipeCall.message
"""

import pytest

from dify_open_webui_adapter import PipeCall
from tests import create_pipe_call_args

# Pytest unit tests  ###########################################################


class TestGet:

    def test1(_):
        body, user, metadata = create_pipe_call_args()

        call = PipeCall(body=body, user=user, metadata=metadata)

        opt = call.message
        assert opt == "Hello Dify"

    def test2(_):
        messages = [
            {"role": "user", "content": "FIRST USER MESSAGE"},
            {"role": "assistant", "content": "FIRST BOT REPLY"},
            {"role": "user", "content": "SECOND USER MESSAGE"},
            {"role": "assistant", "content": "SECOND BOT REPLY"},
            {"role": "user", "content": "THIRD USER MESSAGE"},
        ]

        body, user, metadata = create_pipe_call_args(messages=messages)

        call = PipeCall(body=body, user=user, metadata=metadata)

        opt = call.message
        assert opt == "THIRD USER MESSAGE"

    # err handling  ============================================================

    def test_no_msg(_):
        messages = []

        body, user, metadata = create_pipe_call_args(messages=messages)

        with pytest.raises(ValueError) as exec_info:
            PipeCall(body=body, user=user, metadata=metadata)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("body", "messages")
        assert (
            opt[0]["msg"]
            == "List should have at least 1 item after validation, not 0"
        )
