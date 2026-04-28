"""
pipe-pipe-wf-block_test.py

Unit Tests (using pytest) for:

Pipe.pipe() working with Workflow & blocking
"""

import asyncio
import json
from unittest.mock import patch

import pytest

from tests import convert_key2authorization, create_pipe_call_args

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_block1(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    patch_target = patch_target_post

    mock_resp = mock_chat_wf

    body, user, metadata = create_pipe_call_args(model_id=model_id)

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = asyncio.run(
            pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)
        )

        return replied, mock_post


@pytest.fixture(scope="class")
def testee_block2(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    patch_target = patch_target_post

    mock_resp = mock_chat_wf

    user_dict = {
        "id": "11223344",
        "name": "some user",
        "username": "My Name",
        "email": "123@gmail",
    }

    body, user, metadata = create_pipe_call_args(
        model_id=model_id, user_dict=user_dict
    )

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = asyncio.run(
            pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)
        )

        return replied, mock_post


# Pytest unit tests  ###########################################################


class TestWfBlock1:  # =========================================================

    def test_replied_type(_, testee_block1):
        opt, _ = testee_block1

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_block1):
        opt, _ = testee_block1

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_block1, mock_assertee_chat_wf_block):
        _, mock_post = testee_block1
        assert_args, assert_kwargs = mock_assertee_chat_wf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestWfBlock2:  # =========================================================
    # different user name & answer

    def test_replied_type(_, testee_block2):
        opt, _ = testee_block2

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_block2):
        opt, _ = testee_block2

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_block2, chat_endpoint_wf, auth_key_wf1):
        _, mock_post = testee_block2

        assert_args = [chat_endpoint_wf]

        assert_kwargs = {
            "headers": {
                "Authorization": convert_key2authorization(auth_key_wf1),
                "Content-Type": "application/json",
            },
            "data": json.dumps({
                "inputs": {"query": "Hello Dify"},
                "response_mode": "blocking",
                "user": "some user",
            }),
            "stream": False,
            "timeout": 30,
        }

        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
