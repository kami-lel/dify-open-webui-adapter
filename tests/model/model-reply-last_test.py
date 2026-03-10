"""
model-reply-last_test.py

Unit Tests (using pytest) for:


OWUModel._get_last_user_msg_content()
"""

import pytest


class TestGet:

    def test1(_, model_skip_wf1, pipe_args_no_stream1):
        model = model_skip_wf1
        body, _, _ = pipe_args_no_stream1

        opt = model._get_last_user_msg_content(body)
        print(opt)
        assert opt == "FIRST USER MESSAGE"

    def test2(_, model_skip_cf1, pipe_args_no_stream2):
        model = model_skip_cf1
        body, _, _ = pipe_args_no_stream2

        opt = model._get_last_user_msg_content(body)
        print(opt)
        assert opt == "THIRD USER MESSAGE"

    # err handling  ============================================================

    def test_no_user1(_, model_skip_wf1):
        model = model_skip_wf1
        body = {}

        with pytest.raises(Exception) as exec_info:
            model._get_last_user_msg_content(body)
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""  # BUG
