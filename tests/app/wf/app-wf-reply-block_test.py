"""
app-wf-reply-block_test.py

Unit Tests (using pytest) for:

- WorkflowApp._reply_blocking()
"""

from unittest.mock import Mock, patch


import pytest

from tests import create_test_call


# Pytest fixtures  #############################################################
@pytest.fixture(scope="class")
def testee_dft(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        replied = app._reply_blocking()

        return replied, mock_post


@pytest.fixture(scope="class")
def testee_changed(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    # different output fields
    # TODO
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_test_call(model_id=model_id, stream=False)
    model.call = call

    mock_resp = mock_chat_wf

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

    def test_assert_call(_, testee_changed, mock_assertee_chat_wf_block):
        _, mock_post = testee_changed
        assert_args, assert_kwargs = mock_assertee_chat_wf_block
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestErr:  # ==============================================================

    # FIXME

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
