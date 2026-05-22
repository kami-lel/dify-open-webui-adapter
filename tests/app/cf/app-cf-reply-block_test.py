"""
app-cf-reply-block_test.py

Unit Tests (using pytest) for:

ChatflowApp._reply_blocking()
"""

from unittest.mock import patch

import pytest

from tests import create_mock_resp, create_pipe_call


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def testee_dft(pipe_obj, model_id_cf1, patch_target_post, mock_chat_block_cf):
    model_id = model_id_cf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_block_cf

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

    def test_assert_call(_, testee_dft, mock_assertee_chat_cf_block):
        _, mock_post = testee_dft
        assert_args, assert_kwargs = mock_assertee_chat_cf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestErr:  # ==============================================================

    def test_bad_answ(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        mock_resp_returned_value = {}
        mock_resp = create_mock_resp(return_value=mock_resp_returned_value)

        with (
            patch(patch_target, return_value=mock_resp),
            pytest.raises(KeyError) as exec_info,
        ):
            app._reply_blocking()

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss entry with key 'answer' in Dify chat response:\n{}"
