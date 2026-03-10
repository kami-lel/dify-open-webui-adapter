"""
app-wf-reply-response_test.py

Unit Tests (using pytest) for:

WorkflowApp._open_reply_response()
"""

from unittest.mock import Mock, patch


class TestResponse:

    def test1_no_stream(_, app_skip_wf1, patch_target_post, wf_endpoint):
        replied = "Pseudo Message"

        app = app_skip_wf1
        app.current_user_msg_content = "PRIMARY"
        app.current_enable_stream = False

        mock_resp = Mock()
        mock_resp.json.return_value = {}

        assert_kwargs = {
            "headers": {
                "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                "Content-Type": "application/json",
            },
            "timeout": 30,
        }

        with patch(patch_target_post, return_value=mock_resp) as mock_get:
            opt = app._open_reply_response()

            print(opt)
            assert isinstance(opt, str)
            assert opt == "My Workflow App"

            mock_get.assert_called_once_with(wf_endpoint, **assert_kwargs)

        opt = app._open_reply_response()
        print(opt)
        assert opt == {}

    # err handling  ============================================================

    # TODO
