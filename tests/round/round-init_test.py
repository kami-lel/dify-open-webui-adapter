"""
round-init_test.py

Unit Tests (using pytest) for:

- _StreamingConversationRound.__init__()
"""

from unittest.mock import patch


from dify_open_webui_adapter import _StreamingConversationRound

# pytest  ######################################################################


class TestWf:

    def test_app(_, testee_wf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_wf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.app
            print(opt)
            assert opt is app

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_response(_, testee_wf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_wf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.response
            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_iter_lines(_, testee_wf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_wf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.iter_lines
            print(opt)
            assert opt == []  # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestCf:

    def test_app(_, testee_cf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_cf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.app
            print(opt)
            assert opt is app

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_response(_, testee_cf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_cf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.response
            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_iter_lines(_, testee_cf):
        app, patch_target, mock_resp, assert_args, assert_kwargs = testee_cf

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.iter_lines
            print(opt)
            assert opt == []  # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
