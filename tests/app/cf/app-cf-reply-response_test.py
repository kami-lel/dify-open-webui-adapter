"""
app-cf-reply-response_test.py

Unit Tests (using pytest) for:

ChatflowApp._open_reply_response()
"""

from unittest.mock import patch
import requests


import pytest


class TestResponse:

    def test_no_stream(_, app_skip_cf1, patch_reply_no_stream):
        app = app_skip_cf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        patch_target, mock_resp, assert_args, assert_kwargs = (
            patch_reply_no_stream
        )

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app._open_reply_response()

            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_stream(_, app_skip_cf1, patch_reply_stream):
        app = app_skip_cf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = True

        patch_target, mock_resp, assert_args, assert_kwargs = patch_reply_stream

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app._open_reply_response()

            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # err handling  ============================================================

    def test_bad_connection(_, app_skip_cf1, patch_target_post):
        with patch(
            patch_target_post,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            app = app_skip_cf1

            with pytest.raises(ConnectionError) as exec_info:
                app._open_reply_response()
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"
