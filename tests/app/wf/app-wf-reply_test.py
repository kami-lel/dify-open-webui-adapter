"""
app-wf-reply-block_test.py

Unit Tests (using pytest) for:

WorkflowApp.reply()
"""

from unittest.mock import patch


import pytest

from tests import create_pipe_call


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def testee_dft(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = app.reply()

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


# Todo unit test for stream
