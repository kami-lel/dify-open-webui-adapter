# HACK rm below


"""
round-iter_test.py

Unit Tests (using pytest) for: _StreamingConversationRound:

- .__next__()
- .__iter__()
"""

from unittest.mock import patch


from dify_open_webui_adapter import _StreamingConversationRound


from tests import _convert_lines2list


# tests  #######################################################################
class TestWf:  # ===============================================================

    def test_iter(
        _,
        app_wf_stream,
        patch_target_post,
        assertee_wf_stream,
        mock_wf1,
    ):
        app = app_wf_stream
        patch_target = patch_target_post
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = iter(round)
            assert opt is round

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )

    def test1(
        _, app_wf_stream, patch_target_post, assertee_wf_stream, mock_wf1
    ):
        app = app_wf_stream
        patch_target = patch_target_post
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

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )

    def test1_ping(
        _,
        app_wf_stream,
        patch_target_post,
        assertee_wf_stream,
        mock_wf1,
        stream_entries_wf1,
    ):
        app = app_wf_stream
        patch_target = patch_target_post
        mock_resp = mock_wf1

        lines = _convert_lines2list(stream_entries_wf1)
        lines.insert(0, "event: ping".encode("utf-8"))
        mock_resp.iter_lines.return_value = iter(lines)

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "FIRST RESPONSE MESSAGE",
                "SECOND RESPONSE MESSAGE",
                "THIRD RESPONSE MESSAGE",
            ]

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )

    def test2(
        _, app_wf_stream, patch_target_post, assertee_wf_stream, mock_wf2
    ):
        app = app_wf_stream
        patch_target = patch_target_post
        mock_resp = mock_wf2

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == ["FIRST RESPONSE MESSAGE"]

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )

    def test3(
        _, app_wf_stream, patch_target_post, assertee_wf_stream, mock_wf3
    ):
        app = app_wf_stream
        patch_target = patch_target_post
        mock_resp = mock_wf3

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == ["FIRST RESPONSE MESSAGE"]

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )

    def test4(
        _, app_wf_stream, patch_target_post, assertee_wf_stream, mock_wf4
    ):
        app = app_wf_stream
        patch_target = patch_target_post
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

            mock_post.assert_called_once_with(
                *(assertee_wf_stream[0]), **(assertee_wf_stream[1])
            )


class TestCf:  # ===============================================================

    def test_iter(
        _, app_cf_stream, patch_target_post, assertee_cf_stream, mock_cf1
    ):
        app = app_cf_stream
        patch_target = patch_target_post

        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = iter(round)
            assert opt is round

            mock_post.assert_called_once_with(
                *(assertee_cf_stream[0]), **(assertee_cf_stream[1])
            )

    def test1(
        _, app_cf_stream, patch_target_post, assertee_cf_stream, mock_cf1
    ):
        app = app_cf_stream
        patch_target = patch_target_post
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

            mock_post.assert_called_once_with(
                *(assertee_cf_stream[0]), **(assertee_cf_stream[1])
            )

    def test1_ping(
        _,
        app_cf_stream,
        patch_target_post,
        assertee_cf_stream,
        mock_cf1,
        stream_entries_cf1,
    ):
        app = app_cf_stream
        patch_target = patch_target_post
        mock_resp = mock_cf1

        lines = _convert_lines2list(stream_entries_cf1)
        lines.insert(0, "event: ping".encode("utf-8"))
        mock_resp.iter_lines.return_value = iter(lines)

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round)
            print(opt)
            assert opt == [
                "FIRST RESPONSE MESSAGE",
                "SECOND RESPONSE MESSAGE",
                "THIRD RESPONSE MESSAGE",
            ]

            mock_post.assert_called_once_with(
                *(assertee_cf_stream[0]), **(assertee_cf_stream[1])
            )

    def test2(
        _, app_cf_stream, patch_target_post, assertee_cf_stream, mock_cf2
    ):
        app = app_cf_stream
        patch_target = patch_target_post
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

            mock_post.assert_called_once_with(
                *(assertee_cf_stream[0]), **(assertee_cf_stream[1])
            )

    def test3(
        _, app_cf_stream, patch_target_post, assertee_cf_stream, mock_cf3
    ):
        app = app_cf_stream
        patch_target = patch_target_post
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

            mock_post.assert_called_once_with(
                *(assertee_cf_stream[0]), **(assertee_cf_stream[1])
            )
