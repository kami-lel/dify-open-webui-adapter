"""
rs-err-key_test.py

Unit Tests (using pytest) for:

ResponseStream errors for missing keys
"""

# TODO

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


class TestWf:  # ===============================================================

    def test_event(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        entries = [
            *entries[:-1],
            json.dumps({
                "workflow_run_id": "b790",
                "task_id": "04db",
                "data": {
                    "text": "FIRST RESPONSE MESSAGE",
                    "from_variable_selector": ["4502", "output"],
                },
            }),
        ]
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        # BUG
        assert opt == "miss key in text/event-stream content: 'event'"

    def test_data(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        entries = [
            *entries[:-1],
            json.dumps({
                "event": "text_chunk",
                "workflow_run_id": "b790",
                "task_id": "04db",
            }),
        ]
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        # BUG
        assert opt == "miss key in text/event-stream content: 'data'"
