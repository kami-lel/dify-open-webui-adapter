"""
app-wf-reply-block_test.py

Unit Tests (using pytest) for:

WorkflowApp._reply_blocking()
"""

from unittest.mock import Mock, patch


import pytest


# pytest  ######################################################################
class TestBlock:

    def test_no_stream(_, app_skip_wf1, patch_reply_no_stream):
        app = app_skip_wf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        patch_target, mock_resp, assert_args, assert_kwargs = (
            patch_reply_no_stream
        )

        with patch(patch_target, return_value=mock_resp) as mock_post:
            opt = app._reply_blocking()

            print(opt)
            assert opt == "DIFY REPLIED MESSAGE"

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # err handling  ============================================================

    def test_bad_key1(_, app_skip_wf1, patch_target_post):
        app = app_skip_wf1
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

    def test_bad_key2(_, app_skip_wf1, patch_target_post):
        app = app_skip_wf1
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

    def test_bad_key3(_, app_skip_wf1, patch_target_post):
        app = app_skip_wf1
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
