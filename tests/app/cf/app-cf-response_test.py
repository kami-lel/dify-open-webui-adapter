"""
app-cf-response_test.py

Unit Tests (using pytest) for:

ChatflowApp.open_chat_response() (inherited from BaseDifyApp)
"""

from unittest.mock import patch
import requests


import pytest

from tests import create_pipe_call

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_block(pipe_obj, model_id_cf1, patch_target_post, mock_chat_cf):
    model_id = model_id_cf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_cf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


@pytest.fixture(scope="class")
def testee_stream(pipe_obj, model_id_cf1, patch_target_post, mock_chat_cf):
    model_id = model_id_cf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_cf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


# Pytest unit tests  ###########################################################


class TestBlock:  # ============================================================

    def test_resp_obj(_, testee_block, mock_chat_cf):
        mock_resp, _ = testee_block
        assert mock_resp is mock_chat_cf

    def test_assert_call(_, testee_block, mock_assertee_chat_cf_block):
        _, mock_post = testee_block
        assert_args, assert_kwargs = mock_assertee_chat_cf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestStream:  # ===========================================================

    def test_resp_obj(_, testee_stream, mock_chat_cf):
        mock_resp, _ = testee_stream
        assert mock_resp is mock_chat_cf

    def test_assert_call(_, testee_stream, mock_assertee_chat_cf_stream):
        _, mock_post = testee_stream
        assert_args, assert_kwargs = mock_assertee_chat_cf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestErr:  # ==============================================================

    def test_bad_connection(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        with patch(
            patch_target,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ), pytest.raises(ConnectionError) as exec_info:
            app.open_chat_response()

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "fail to connect Dify: Bad Connection"
