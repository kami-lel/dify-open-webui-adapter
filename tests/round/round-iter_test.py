"""
round-iter_test.py

Unit Tests (using pytest) for: _StreamingConversationRound:

- .__next__()
- .__iter__()
"""

from unittest.mock import patch


from dify_open_webui_adapter import _StreamingConversationRound


# tests  #######################################################################
class TestWf:  # ===============================================================

    def test_iter(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = iter(round)
            assert opt is round

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test1(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "FIRST RESPONSE MESSAGE",
                "SECOND RESPONSE MESSAGE",
                "THIRD RESPONSE MESSAGE",
            ]

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test2(_, testee_wf, mock_wf2):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf2

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == ["FIRST RESPONSE MESSAGE"]

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test3(_, testee_wf, mock_wf3):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf3

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == []  # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test4(_, testee_wf, mock_wf4):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf4

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "Once",
                " upon",
                " a",
                " time",
                ",",
                " in",
                " a",
                " quiet",
                " village",
                " nestled",
                " between",
                " rolling",
                " hills",
                ",",
                " there",
                " lived",
                " a",
                " curious",
                " young",
                " girl",
                " named",
                " Lily",
                ".",
                " Every",
                " day",
                ",",
                " she",
                " explored",
                " the",
                " me",
                "adows",
                ",",
                " collecting",
                " wild",
                "flowers",
                " and",
                " listening",
                " to",
                " the",
                " songs",
                " of",
                " birds",
                ".\n\n",
                "The",
                " fair",
                "ies",
                " welcomed",
                " Lily",
                " with",
                " smiles",
                " and",
                " showed",
                " her",
                " their",
                " magical",
                " garden",
                ".",
            ]
            # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestCf:  # ===============================================================

    def test_iter(_, testee_cf, mock_cf1):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = iter(round)
            assert opt is round

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test1(_, testee_cf, mock_cf1):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "FIRST RESPONSE MESSAGE",
                "SECOND RESPONSE MESSAGE",
                "THIRD RESPONSE MESSAGE",
            ]

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test2(_, testee_cf, mock_cf2):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf2

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "Hello",
                "!",
                " I'm",
                " here",
                " to",
                " assist",
                " you",
                " with",
                " any",
                " questions",
                " or",
                " tasks",
                " you",
                " have",
                ".",
                " Feel",
                " free",
                " to",
                " ask",
                " me",
                " anything",
                "!",
                "",
                "",
            ]
            # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test3(_, testee_cf, mock_cf3):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf3

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "BST",
                " algorithm",
                ":",
                "  \n",
                "-",
                " **",
                "Insert",
                ":**",
                " Compare",
                " value",
                ",",
                " go",
                " left",
                " if",
                " smaller",
                ",",
                " right",
                " if",
                " larger",
                ",",
                " until",
                " None",
                ",",
                " insert",
                " node",
            ]
            # BUG

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
