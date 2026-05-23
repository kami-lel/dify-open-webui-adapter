"""
app-wf-reply_blocking_test.py

Unit Tests (using pytest) for:

WorkflowApp._reply_blocking()
"""

import json
from unittest.mock import patch


import pytest

from tests import (
    convert_key2authorization,
    create_mock_resp_block,
    create_pipe_call,
)


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def testee_dft(pipe_obj, model_id_wf1, patch_target_post, mock_chat_block_wf):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_block_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = app._reply_blocking()

        return replied, mock_post


@pytest.fixture(scope="class")
def testee_changed(pipe_obj, model_id_wf2, patch_target_post):
    # different output fields
    model_id = model_id_wf2
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=False)
    model.call = call

    returned_value = {"data": {"outputs": {"Output": "DIFY REPLIED MESSAGE"}}}
    mock_resp = create_mock_resp_block(return_value=returned_value)

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = app._reply_blocking()

        return replied, mock_post


# Pytest unit tests  ###########################################################


class TestBlock:  # ============================================================

    def test_replied_type(_, testee_dft):
        opt, _ = testee_dft

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_dft):
        opt, _ = testee_dft

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_dft, mock_assertee_chat_wf_block):
        _, mock_post = testee_dft
        assert_args, assert_kwargs = mock_assertee_chat_wf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestChg:  # ==============================================================

    def test_replied_type(_, testee_changed):
        opt, _ = testee_changed

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_changed):
        opt, _ = testee_changed

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_changed, chat_endpoint_wf, auth_key_wf2):
        _, mock_post = testee_changed

        assert_args = [chat_endpoint_wf]
        assert_kwargs = {
            "headers": {
                "Authorization": convert_key2authorization(auth_key_wf2),
                "Content-Type": "application/json",
            },
            "data": json.dumps({
                "inputs": {"Input": "Hello Dify"},
                "response_mode": "blocking",
                "user": "user",
            }),
            "stream": False,
            "timeout": 30,
        }
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestErr:  # ==============================================================

    def test_bad_key1(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        mock_resp_returned_value = {}
        mock_resp = create_mock_resp_block(
            return_value=mock_resp_returned_value
        )

        with (
            patch(patch_target, return_value=mock_resp),
            pytest.raises(KeyError) as exec_info,
        ):
            app._reply_blocking()

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss entry with key 'data' in Dify chat response:\n{}"

    def test_bad_key2(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        returned_value = {"data": {}}
        mock_resp = create_mock_resp_block(return_value=returned_value)

        with (
            patch(patch_target, return_value=mock_resp),
            pytest.raises(KeyError) as exec_info,
        ):
            app._reply_blocking()

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "miss entry with key 'outputs' in Dify chat response:\n"
            "{'data': {}}"
        )

    def test_bad_key3(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        returned_value = {"data": {"outputs": {}}}
        mock_resp = create_mock_resp_block(return_value=returned_value)

        with (
            patch(patch_target, return_value=mock_resp),
            pytest.raises(KeyError) as exec_info,
        ):
            app._reply_blocking()

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "miss entry with key 'answer' in Dify chat response:\n"
            "{'data': {'outputs': {}}}"
        )
