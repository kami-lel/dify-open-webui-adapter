"""
app-wf-reply-block_test.py

Unit Tests (using pytest) for:

- WorkflowApp._reply_blocking()
"""

# FIXME

import json
from unittest.mock import Mock, patch


import pytest

from tests import create_mock_resp, create_test_call


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def testee_dft(pipe_obj, model_id_wf1, patch_target_post):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = create_mock_resp(return_value=None)  # Hack use return value

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = app._reply_blocking()

        return replied, mock_post


# Pytest unit tests  ###########################################################


class TestBlock:

    def test_replied_type(_, testee_dft):
        opt, _ = testee_dft

        print(opt)
        assert isinstance(opt, str)

    def test_assert_call(_, testee_dft, chat_endpoint_wf, authorization_wf1):
        _, mock_post = testee_dft
        mock_post.assert_called_once_with(
            chat_endpoint_wf,
            headers={
                "Authorization": authorization_wf1,
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "inputs": {"query": "Hello Dify"},
                "response_mode": "blocking",
                "user": "user",
            }),
            stream=False,
            timeout=30,
        )


# pytest  ######################################################################
class ATestBlock:

    def test_dft(
        _, app_wf_skip1, patch_target_post, mock_block_wf, assertee_wf_block
    ):
        app = app_wf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False
        patch_target = patch_target_post
        mock_resp = mock_block_wf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app._reply_blocking()

            print(opt)
            assert opt == "DIFY REPLIED MESSAGE"

            mock_post.assert_called_once_with(
                *(assertee_wf_block[0]), **(assertee_wf_block[1])
            )

    def test_changed(
        _,
        app_changed_input,
        patch_target_post,
        mock_block_wf,
        assertee_wf_block,
    ):
        app = app_changed_input
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        patch_target = patch_target_post
        mock_resp = mock_block_wf

        assert_kwargs = assertee_wf_block[1]
        assert_kwargs["data"] = json.dumps({
            "inputs": {"Input": "PRIMARY"},
            "response_mode": "blocking",
            "user": "user",
        })

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app._reply_blocking()

            print(opt)
            assert opt == "DIFY REPLIED MESSAGE"

            mock_post.assert_called_once_with(
                *(assertee_wf_block[0]), **assert_kwargs
            )

    # err handling  ============================================================

    def test_bad_key1(_, app_wf_skip1, patch_target_post):
        app = app_wf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {}

        with patch(patch_target_post, return_value=mock_resp):
            with pytest.raises(KeyError) as exec_info:
                app._reply_blocking()

            opt = exec_info.value.args[0]
            print(opt)
            assert opt == "miss key in Dify response: data"

    def test_bad_key2(_, app_wf_skip1, patch_target_post):
        app = app_wf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"data": {}}

        with patch(patch_target_post, return_value=mock_resp):
            with pytest.raises(KeyError) as exec_info:
                app._reply_blocking()

            opt = exec_info.value.args[0]
            print(opt)
            assert opt == "miss key in Dify response: outputs"

    def test_bad_key3(_, app_wf_skip1, patch_target_post):
        app = app_wf_skip1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"data": {"outputs": {}}}

        with patch(patch_target_post, return_value=mock_resp):
            with pytest.raises(KeyError) as exec_info:
                app._reply_blocking()

            opt = exec_info.value.args[0]
            print(opt)
            assert opt == "miss key in Dify response: answer"
