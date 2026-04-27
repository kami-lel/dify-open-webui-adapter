"""
app-wf-response_test.py

Unit Tests (using pytest) for:

WorkflowApp.open_chat_response() (inherited from BaseDifyApp)
"""

# FIXME

import json
from unittest.mock import Mock, patch
import requests


import pytest


from tests import create_test_call, create_mock_resp

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_no_stream(pipe_obj, model_id_wf1, patch_target_post):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = create_mock_resp(return_value=None)  # Hack use return value

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


@pytest.fixture
def testee_reply_block(patch_target_post, endpoint_wf, authorization_wf1):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"ok": True}
    mock_resp.text = "APP REPLIED MESSAGE"

    assert_args = [endpoint_wf]

    assert_kwargs = {
        "headers": {
            "Authorization": authorization_wf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps({
            "inputs": {"query": "PRIMARY"},
            "response_mode": "streaming",
            "user": "user",
        }),
        "stream": True,
        "timeout": 300,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs


# Pytest unit tests  ###########################################################
class TestNoStream:  # =========================================================

    # Hack unit test for response obj

    def test_resp_obj(_):
        pass

    def test_assert_url(
        _, testee_no_stream, chat_endpoint_wf, authorization_wf1
    ):
        _, mock_post = testee_no_stream
        mock_post.assert_called_once_with(
            chat_endpoint_wf,
            headers={
                "Authorization": authorization_wf1,
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
            data=json.dumps({
                "inputs": {"query": "PRIMARY"},
                "response_mode": "streaming",
                "user": "user",
            }),
            stream=True,
            timeout=300,
        )


class TestResponse:

    def test_no_stream(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        mock_resp = create_mock_resp(return_value=None)  # Hack use return value

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app.open_chat_response()

            print(opt)
            assert opt is mock_resp

            mock_post.assert_called_once_with(
                *(assertee_wf_block[0]), **(assertee_wf_block[1])
            )

    def test_stream(_, app_wf_skip1, testee_reply_block):
        app = app_wf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = True

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"ok": True}
        mock_resp.text = "Pseudo Message"

        patch_target, mock_resp, assert_args, assert_kwargs = testee_reply_block

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app.open_reply_response()

            print(opt)
            assert opt is mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # err handling  ============================================================

    def test_bad_connection(_, app_wf_skip1, patch_target_post):
        with patch(
            patch_target_post,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            app = app_wf_skip1

            with pytest.raises(ConnectionError) as exec_info:
                app.open_reply_response()
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"
