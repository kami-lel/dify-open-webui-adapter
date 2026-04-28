"""
app-wf-response_test.py

Unit Tests (using pytest) for:

WorkflowApp.open_chat_response() (inherited from BaseDifyApp)
"""

import json
from unittest.mock import Mock, patch
import requests


import pytest


from tests import create_test_call, create_mock_resp

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_no_stream(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


@pytest.fixture(scope="class")
def testee_stream(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


# Pytest unit tests  ###########################################################
class TestNoStream:  # =========================================================

    def test_resp_obj(_, testee_no_stream, mock_chat_wf):
        mock_resp, _ = testee_no_stream
        assert mock_resp is mock_chat_wf

    def test_assert_call(_, testee_no_stream, mock_assertee_chat_wf_block):
        _, mock_post = testee_no_stream
        assert_args, assert_kwargs = mock_assertee_chat_wf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestStream:  # ===========================================================

    def test_resp_obj(_, testee_stream, mock_chat_wf):
        mock_resp, _ = testee_stream
        assert mock_resp is mock_chat_wf

    def test_assert_call(_, testee_stream, mock_assertee_chat_wf_stream):
        _, mock_post = testee_stream
        assert_args, assert_kwargs = mock_assertee_chat_wf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestErr:  # ==============================================================

    def test_bad_connection(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        with patch(
            patch_target,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ), pytest.raises(ConnectionError) as exec_info:
            app.open_chat_response()

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "fail to connect Dify: Bad Connection"
