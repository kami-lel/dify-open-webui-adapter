"""
rs-next-wf_test.py

Unit Tests (using pytest) for:

.__next__() using wf
"""

from unittest.mock import patch

import pytest

from dify_open_webui_adapter import ResponseStream
from tests import (
    create_mock_resp_stream,
    create_pipe_call,
    load_stream_entries_testee,
)

# Pytest unit tests  ###########################################################


class TestNext:

    def test1(_, testee_wf1):
        sr, _ = testee_wf1

        assert next(sr) == "FIRST RESPONSE MESSAGE"
        assert next(sr) == "SECOND RESPONSE MESSAGE"
        assert next(sr) == "THIRD RESPONSE MESSAGE"
        with pytest.raises(StopIteration):
            next(sr)


class TestList:

    def test1(_, testee_wf1):
        sr, _ = testee_wf1

        entries = list(sr)
        print(entries)

        assert entries == [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

    def test1_ping(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf1")
        entries.insert(0, "event: ping")
        mock_resp = create_mock_resp_stream(entries)

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)

            assert entries == [
                "FIRST RESPONSE MESSAGE",
                "SECOND RESPONSE MESSAGE",
                "THIRD RESPONSE MESSAGE",
            ]

    def test2(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf2")
        mock_resp = create_mock_resp_stream(entries)

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)
            assert entries == ["FIRST RESPONSE MESSAGE"]

    def test3(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf3")
        mock_resp = create_mock_resp_stream(entries)

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)
            assert entries == ["FIRST RESPONSE MESSAGE"]

    def test4(_, pipe_obj, model_id_wf1, patch_target_post):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        entries = load_stream_entries_testee("wf4")
        mock_resp = create_mock_resp_stream(entries)

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)
            assert entries == [
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
