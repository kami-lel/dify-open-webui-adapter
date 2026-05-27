"""
rs-err_test.py

Unit Tests (using pytest) for:

ResponseStream errors
"""

# Pytest unit tests  ###########################################################


from unittest.mock import MagicMock, patch

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


class TestUnicode:  # ==========================================================

    def test_wf(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        mock_resp = MagicMock()
        mock_resp.status_code = 201

        encoded = [ll.encode(encoding="utf-16") for ll in entries]

        mock_resp.iter_lines.return_value = iter(encoded)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )

    def test_cf(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("cf1")
        mock_resp = MagicMock()
        mock_resp.status_code = 201

        encoded = [ll.encode(encoding="utf-16") for ll in entries]

        mock_resp.iter_lines.return_value = iter(encoded)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )


class TestJSONDecode:  # =======================================================

    def test_wf(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_json = 'data: {"text": "value'

        entries = load_stream_entries_testee("wf1")
        entries.insert(0, bad_json)

        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == """fail to parse text/event-stream as JSON: Unterminated string starting at: line 1 column 10 (char 9): b'data: {"text": "value'"""
        )

    def test_cf(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        bad_json = 'data: {"text": "value'

        entries = load_stream_entries_testee("cf1")
        entries.insert(0, bad_json)
        mock_resp = create_mock_resp_stream(entries)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                list(ResponseStream(app))

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == """fail to parse text/event-stream as JSON: Unterminated string starting at: line 1 column 10 (char 9): b'data: {"text": "value'"""
        )
