"""
rs-err-key_test.py

Unit Tests (using pytest) for:

ResponseStream errors for missing keys
"""

# Pytest unit tests  ###########################################################


import json
from unittest.mock import patch

import pytest

from dify_open_webui_adapter import ResponseStream
from tests import (
    create_mock_resp_stream,
    create_pipe_call,
    load_stream_entries_testee,
)


# BUG
class TestWf:  # ===============================================================

    def test_event(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        bad_entry = {
            "workflow_run_id": "b790",
            "task_id": "04db",
            "data": {
                "text": "FIRST RESPONSE MESSAGE",
                "from_variable_selector": ["4502", "output"],
            },
        }
        entries[-1] = json.dumps(bad_entry)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'event'"

    def test_data(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_entry = {
            "event": "text_chunk",
            "workflow_run_id": "b790",
            "task_id": "04db",
        }

        entries = load_stream_entries_testee("wf1")
        entries[-1] = json.dumps(bad_entry)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'data'"

    def test_text(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_entry = {
            "event": "text_chunk",
            "workflow_run_id": "b790",
            "task_id": "04db",
            "data": {
                "from_variable_selector": ["4502", "output"],
            },
        }
        entries = load_stream_entries_testee("wf1")
        entries[-1] = json.dumps(bad_entry)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'text'"


class TestCf:  # ===============================================================

    def test_event(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_entry = {
            "conversation_id": "c0cf",
            "message_id": "ff06",
            "created_at": 1768046345,
            "task_id": "5863",
            "id": "ff06",
            "answer": "FIRST RESPONSE MESSAGE",
            "from_variable_selector": ["llm", "text"],
        }
        entries = load_stream_entries_testee("cf1")
        entries[-1] = json.dumps(bad_entry)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'event'"

    def test_answer(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_entry = {
            "event": "message",
            "conversation_id": "c0cf",
            "message_id": "ff06",
            "created_at": 1768046345,
            "task_id": "5863",
            "id": "ff06",
            "from_variable_selector": ["llm", "text"],
        }
        entries = load_stream_entries_testee("cf1")
        entries[-1] = json.dumps(bad_entry)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "miss key in text/event-stream content: 'answer'"
