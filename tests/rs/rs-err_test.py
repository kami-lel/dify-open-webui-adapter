"""
rs-err_test.py

Unit Tests (using pytest) for:

ResponseStream errors
"""

# Pytest unit tests  ###########################################################


from unittest.mock import patch

import pytest

from dify_open_webui_adapter import ResponseStream

from tests import (
    create_mock_resp_stream,
    create_pipe_call,
    load_stream_entries_testee,
)


class TestExhaust:  # ==========================================================

    def test_wf(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        entries = entries[:-1]
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "exhaust text/event-stream without ending event"

    def test_cf(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("cf1")
        entries = entries[:-1]
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "exhaust text/event-stream without ending event"

    # TODO more tests
