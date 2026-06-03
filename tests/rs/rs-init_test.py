"""
sr-init_test.py

Unit Tests (using pytest) for:

ResponseStream.__init__()
"""

from dify_open_webui_adapter import ResponseStream

# BUG BUG

# Pytest unit tests  ###########################################################


class TestConst:

    def test1(_):
        assert ResponseStream._TEXT_STREAM_ENCODING == "utf-8"

    def test2(_):
        assert ResponseStream._STREAM_PREFIX == "data: "


class TestWf:  # ===============================================================

    # test .app  ---------------------------------------------------------------
    def test_app(_, testee_wf1, pipe_obj, model_id_wf1):
        testee = testee_wf1
        sr, _ = testee
        app = sr.app

        assert app is pipe_obj.apps[model_id_wf1]

    # test .response  ----------------------------------------------------------
    def test_resp_obj(_, testee_wf1, mock_chat_stream_wf1):
        testee = testee_wf1
        sr, _ = testee
        resp = sr.response

        assert resp is mock_chat_stream_wf1

    def test_assert_call(_, testee_wf1, mock_assertee_chat_wf_stream):
        testee = testee_wf1
        _, mock_post = testee
        assert_args, assert_kwargs = mock_assertee_chat_wf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # test .iter_lines  --------------------------------------------------------
    def test_lines(_, testee_wf1):
        testee = testee_wf1
        sr, _ = testee
        lines = list(sr.iter_lines)

        print(lines)
        assert lines == [
            (
                b'data: {"event": "text_chunk", "workflow_run_id": "b790",'
                b' "task_id": "04db", "data": {"text": "FIRST RESPONSE'
                b' MESSAGE", "from_variable_selector": ["4502", "output"]}}'
            ),
            (
                b'data: {"event": "text_chunk", "workflow_run_id": "b790",'
                b' "task_id": "04db", "data": {"text": "SECOND RESPONSE'
                b' MESSAGE", "from_variable_selector": ["4502", "output"]}}'
            ),
            (
                b'data: {"event": "text_chunk", "workflow_run_id": "b790",'
                b' "task_id": "04db", "data": {"text": "THIRD RESPONSE'
                b' MESSAGE", "from_variable_selector": ["4502", "output"]}}'
            ),
            (
                b'data: {"event": "workflow_finished", "workflow_run_id":'
                b' "b790", "task_id": "04db", "data": {}}'
            ),
        ]


class TestCf:  # ==============================================================

    # test .app  ---------------------------------------------------------------
    def test_app(_, testee_cf1, pipe_obj, model_id_cf1):
        testee = testee_cf1
        sr, _ = testee
        app = sr.app

        assert app is pipe_obj.apps[model_id_cf1]

    # test .response  ----------------------------------------------------------
    def test_resp_obj(_, testee_cf1, mock_chat_stream_cf1):
        testee = testee_cf1
        sr, _ = testee
        resp = sr.response

        assert resp is mock_chat_stream_cf1

    def test_assert_call(_, testee_cf1, mock_assertee_chat_cf_stream):
        testee = testee_cf1
        _, mock_post = testee
        assert_args, assert_kwargs = mock_assertee_chat_cf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # test .iter_lines  --------------------------------------------------------
    def test_lines(_, testee_cf1):
        testee = testee_cf1
        sr, _ = testee
        lines = list(sr.iter_lines)

        print(lines)
        assert lines == [
            (
                b'data: {"event": "message", "conversation_id": "c0cf",'
                b' "message_id": "ff06", "created_at": 1768046345, "task_id":'
                b' "5863", "id": "ff06", "answer": "FIRST RESPONSE MESSAGE",'
                b' "from_variable_selector": ["llm", "text"]}'
            ),
            (
                b'data: {"event": "message", "conversation_id": "c0cf",'
                b' "message_id": "ff06", "created_at": 1768046345, "task_id":'
                b' "5863", "id": "ff06", "answer": "SECOND RESPONSE MESSAGE",'
                b' "from_variable_selector": ["llm", "text"]}'
            ),
            (
                b'data: {"event": "message", "conversation_id": "c0cf",'
                b' "message_id": "ff06", "created_at": 1768046345, "task_id":'
                b' "5863", "id": "ff06", "answer": "THIRD RESPONSE MESSAGE",'
                b' "from_variable_selector": ["llm", "text"]}'
            ),
            (
                b'data: {"event": "workflow_finished", "conversation_id":'
                b' "c0cf", "message_id": "ff06", "created_at": 1768046345,'
                b' "task_id": "5863", "workflow_run_id": "561d", "data": {}}'
            ),
        ]
