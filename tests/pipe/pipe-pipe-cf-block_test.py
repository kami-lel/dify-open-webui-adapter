"""
pipe-pipe-cf-block_test.py

Unit Tests (using pytest) for:

Pipe.pipe() working with Chatflow & blocking
"""

import asyncio
from unittest.mock import patch

import pytest

from tests import create_pipe_call_args

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_block1(
    pipe_obj, model_id_cf1, patch_target_post, mock_chat_block_cf
):
    model_id = model_id_cf1
    patch_target = patch_target_post

    mock_resp = mock_chat_block_cf

    body, user, metadata = create_pipe_call_args(model_id=model_id)

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = asyncio.run(
            pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)
        )

        return replied, mock_post


# Pytest unit tests  ###########################################################


class TestcfBlock1:  # =========================================================

    def test_replied_type(_, testee_block1):
        opt, _ = testee_block1

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_block1):
        opt, _ = testee_block1

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_block1, mock_assertee_chat_cf_block):
        _, mock_post = testee_block1
        assert_args, assert_kwargs = mock_assertee_chat_cf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
