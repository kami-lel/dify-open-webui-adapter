"""
sr-init_test.py

Unit Tests (using pytest) for:

ResponseStream.__init__()
"""

from unittest.mock import patch


import pytest


from dify_open_webui_adapter import ResponseStream

from tests import create_pipe_call

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_wf(pipe_obj, model_id_wf1, patch_target_post, mock_chat_stream_wf1):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_stream_wf1

    with patch(patch_target, return_value=mock_resp) as mock_post:
        sr = ResponseStream(app)

        return sr, mock_post


@pytest.fixture(scope="class")
def testee_cf(pipe_obj, model_id_cf1, patch_target_post, mock_chat_stream_cf1):
    model_id = model_id_cf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_stream_cf1

    with patch(patch_target, return_value=mock_resp) as mock_post:
        sr = ResponseStream(app)

        return sr, mock_post


# Pytest unit tests  ###########################################################


class TestConst:

    def test1(_):
        assert ResponseStream._TEXT_STREAM_ENCODING == "utf-8"

    def test2(_):
        assert ResponseStream._STREAM_PREFIX == "data: "


class TestWf:  # ===============================================================

    # test .app  ---------------------------------------------------------------
    def test_app(_, testee_wf, pipe_obj, model_id_wf1):
        testee = testee_wf
        sr, _ = testee
        app = sr.app

        assert app is pipe_obj.apps[model_id_wf1]

    # test .response  ----------------------------------------------------------
    def test_resp_obj(_, testee_wf, mock_chat_stream_wf1):
        testee = testee_wf
        sr, _ = testee
        resp = sr.response

        assert resp is mock_chat_stream_wf1

    def test_assert_call(_, testee_wf, mock_assertee_chat_wf_stream):
        testee = testee_wf
        _, mock_post = testee
        assert_args, assert_kwargs = mock_assertee_chat_wf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # test .iter_lines  --------------------------------------------------------
    def test_lines(_, testee_wf):
        testee = testee_wf
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
    def test_app(_, testee_cf, pipe_obj, model_id_cf1):
        testee = testee_cf
        sr, _ = testee
        app = sr.app

        assert app is pipe_obj.apps[model_id_cf1]

    # test .response  ----------------------------------------------------------
    def test_resp_obj(_, testee_cf, mock_chat_stream_cf1):
        testee = testee_cf
        sr, _ = testee
        resp = sr.response

        assert resp is mock_chat_stream_cf1

    def test_assert_call(_, testee_cf, mock_assertee_chat_cf_stream):
        testee = testee_cf
        _, mock_post = testee
        assert_args, assert_kwargs = mock_assertee_chat_cf_stream
        mock_post.assert_called_once_with(*assert_args, **assert_kwargs)

    # test .iter_lines  --------------------------------------------------------
    def test_lines(_, testee_cf):
        testee = testee_cf
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
