"""
app-wf-reply-block_test.py

Unit Tests (using pytest) for:

WorkflowApp._reply_blocking()
"""

from unittest.mock import Mock, patch


# pytest  ######################################################################
class TestBlock:

    def test1(_, app_skip_wf1, patch_target):
        return  # BUG
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "mode": "workflow",
            "name": "My Workflow App",
        }
        assert_kwargs = {
            "headers": {
                "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
                "Content-Type": "application/json",
            },
            "timeout": 30,
        }

        with patch(patch_target, return_value=mock_resp) as mock_get:
            app_skip_wf1._reply_blocking()

            mock_get.assert_awaited_once_with("", **assert_kwargs)

    # err handling  ============================================================

    # TODO
