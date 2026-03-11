"""
app-wf-reply-response_test.py

Unit Tests (using pytest) for:

WorkflowApp._open_reply_response()
"""

from unittest.mock import Mock, patch
import requests
import pytest


class TestResponse:

    def test1_no_stream(_, app_skip_wf1, patch_target_post, wf_endpoint):
        app = app_skip_wf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"ok": True}
        mock_resp.text = "Pseudo Message"

        with patch(patch_target_post, return_value=mock_resp) as mock_post:
            opt = app._open_reply_response()

            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(
                wf_endpoint,
                headers={
                    "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                    "Content-Type": "application/json",
                },
                data=(
                    '{"inputs": {"query": "PRIMARY"}, '
                    '"response_mode": "blocking", '
                    '"user": "user"}'
                ),
                stream=False,
                timeout=30,
            )

    def test1_stream(_, app_skip_wf1, patch_target_post, wf_endpoint):
        app = app_skip_wf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = True

        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"ok": True}
        mock_resp.text = "Pseudo Message"

        with patch(patch_target_post, return_value=mock_resp) as mock_post:
            opt = app._open_reply_response()

            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(
                wf_endpoint,
                headers={
                    "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                data=(
                    '{"inputs": {"query": "PRIMARY"}, '
                    '"response_mode": "streaming", '
                    '"user": "user"}'
                ),
                stream=True,
                timeout=300,
            )

    # err handling  ============================================================

    def test_bad_connection(_, app_skip_wf1, patch_target_post):
        with patch(
            patch_target_post,
            side_effect=requests.exceptions.ConnectionError("Bad Connection"),
        ):
            app = app_skip_wf1

            with pytest.raises(ConnectionError) as exec_info:
                app._open_reply_response()
            opt = exec_info.value.args[0]

            print(opt)
            assert opt == "fail request to Dify: Bad Connection"
