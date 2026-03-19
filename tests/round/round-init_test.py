"""
round-init_test.py

Unit Tests (using pytest) for:

- _StreamingConversationRound.__init__()
"""

from unittest.mock import patch


from dify_open_webui_adapter import _StreamingConversationRound

# pytest  ######################################################################


class TestWf:

    def test_app(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.app
            print(opt)
            assert opt is app

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_response(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.response
            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_iter_lines(_, testee_wf, mock_wf1):
        app, patch_target, assert_args, assert_kwargs = testee_wf
        mock_resp = mock_wf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round.iter_lines)
            print(opt)
            assert opt == [
                (
                    b'data: {"event": "text_chunk", '
                    b'"workflow_run_id": "b790", '
                    b'"task_id": "04db", '
                    b'"data": {"text": "FIRST RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["4502", "output"]}}'
                ),
                (
                    b'data: {"event": "text_chunk", '
                    b'"workflow_run_id": "b790", '
                    b'"task_id": "04db", '
                    b'"data": {"text": "SECOND RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["4502", "output"]}}'
                ),
                (
                    b'data: {"event": "text_chunk", '
                    b'"workflow_run_id": "b790", '
                    b'"task_id": "04db", '
                    b'"data": {"text": "THIRD RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["4502", "output"]}}'
                ),
                (
                    b'data: {"event": "workflow_finished", '
                    b'"workflow_run_id": "b790", '
                    b'"task_id": "04db", '
                    b'"data": {}}'
                ),
            ]

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)


class TestCf:

    def test_app(_, testee_cf, mock_cf1):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.app
            print(opt)
            assert opt is app

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_response(_, testee_cf, mock_cf1):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = round.response
            print(opt)
            assert opt == mock_resp

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    def test_iter_lines(_, testee_cf, mock_cf1):
        app, patch_target, assert_args, assert_kwargs = testee_cf
        mock_resp = mock_cf1

        with patch(patch_target, return_value=mock_resp) as mock_post:
            round = _StreamingConversationRound(app)

            opt = list(round.iter_lines)
            print(opt)
            assert opt == [
                (
                    b'data: {"event": "message", '
                    b'"conversation_id": "c0cf", '
                    b'"message_id": "ff06", '
                    b'"created_at": 1768046345,'
                    b' "task_id": "5863", '
                    b'"id": "ff06", '
                    b'"answer": "FIRST '
                    b'RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["llm", "text"]}'
                ),
                (
                    b'data: {"event": "message", '
                    b'"conversation_id": "c0cf", '
                    b'"message_id": "ff06", '
                    b'"created_at": 1768046345, '
                    b'"task_id": "5863", '
                    b'"id": "ff06", '
                    b'"answer": "SECOND RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["llm", "text"]}'
                ),
                (
                    b'data: {"event": "message", '
                    b'"conversation_id": "c0cf", '
                    b'"message_id": "ff06", '
                    b'"created_at": 1768046345, '
                    b'"task_id": "5863", '
                    b'"id": "ff06", '
                    b'"answer": "THIRD RESPONSE MESSAGE", '
                    b'"from_variable_selector": ["llm", "text"]}'
                ),
                (
                    b'data: {"event": "workflow_finished", '
                    b'"conversation_id": "c0cf", '
                    b'"message_id": "ff06", '
                    b'"created_at": 1768046345, '
                    b'"task_id": "5863", '
                    b'"workflow_run_id": "561d", '
                    b'"data": {}}'
                ),
            ]

            mock_post.assert_called_once_with(*assert_args, **assert_kwargs)
