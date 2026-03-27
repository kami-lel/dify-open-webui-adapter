"""
app-cf-reply-response_test.py

Unit Tests (using pytest) for:

ChatflowApp.open_reply_response()
"""

from unittest.mock import patch, Mock
import json
import requests


import pytest


# Pytest fixtures  #############################################################
@pytest.fixture
def testee_stream(patch_target_post, endpoint_cf, authorization_cf1):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"ok": True}
    mock_resp.text = "APP REPLIED MESSAGE"

    assert_args = [endpoint_cf]

    assert_kwargs = {
        "headers": {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps({
            "query": "PRIMARY",
            "response_mode": "streaming",
            "user": "user",
            "conversation_id": "",
            "auto_generate_name": False,
            "inputs": {},
        }),
        "stream": True,
        "timeout": 300,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs


# Pytest unit tests  ###########################################################
class TestResponse:

    def test_no_stream(_, app_cf_skip1, testee_block):
        app = app_cf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        patch_target, mock_resp, assert_args, assert_kwargs = testee_block

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app.open_reply_response()

            print(opt)
            assert opt is mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_stream(_, app_cf_skip1, testee_stream):
        app = app_cf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = True

        patch_target, mock_resp, assert_args, assert_kwargs = testee_stream

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app.open_reply_response()

            print(opt)
            assert opt is mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # err handling  ============================================================

    def test_bad_connection(_, app_cf_skip1, patch_target_post):
        with patch(
            patch_target_post,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            app = app_cf_skip1

            with pytest.raises(ConnectionError) as exec_info:
                app.open_reply_response()
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"
