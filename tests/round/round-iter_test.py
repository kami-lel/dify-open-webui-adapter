"""
round-iter_test.py

Unit Tests (using pytest) for: _StreamingConversationRound:

- .__next__()
- .__iter__()
"""

from unittest.mock import patch


from dify_open_webui_adapter import _StreamingConversationRound


# tests  #######################################################################
class TestWf:

    def test_iter(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = iter(round)
            assert opt is round

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test1(_):
        pass  # TODO
