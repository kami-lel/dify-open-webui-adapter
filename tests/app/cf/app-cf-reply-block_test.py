"""
app-cf-reply-block_test.py

Unit Tests (using pytest) for:

ChatflowApp._reply_blocking()
"""

from unittest.mock import Mock, patch


import pytest


# pytest  ######################################################################
class TestBlock:

    def test_no_stream(_, app_skip_cf1, patch_reply_no_stream):
        # BUG BUG
        app = app_skip_cf1
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

    # TODO TODO
