"""
pipe-pipe_test.py

Unit Tests (using pytest) for:

Pipe.pipe()
"""

# Todo complete unit tests

import asyncio
from unittest.mock import patch

import pytest

from tests import create_test_call_args

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_wf_block(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    patch_target = patch_target_post

    mock_resp = mock_chat_wf

    body, user, metadata = create_test_call_args(model_id=model_id)

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = asyncio.run(
            pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)
        )

        return replied, mock_post


# Pytest unit tests  ###########################################################


class TestWfBlock:  # ==========================================================

    def test_replied_type(_, testee_wf_block):
        opt, _ = testee_wf_block

        print(opt)
        assert isinstance(opt, str)

    def test_replied_content(_, testee_wf_block):
        opt, _ = testee_wf_block

        assert opt == "DIFY REPLIED MESSAGE"

    def test_assert_call(_, testee_wf_block, mock_assertee_chat_wf_block):
        _, mock_post = testee_wf_block
        assert_args, assert_kwargs = mock_assertee_chat_wf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
