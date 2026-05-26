"""
rs-next_test.py

Unit Tests (using pytest) for:

- .__next__()

using stream_entries_wf1.json
"""

# TODO


# Pytest unit tests  ###########################################################


from unittest.mock import patch

from dify_open_webui_adapter import ResponseStream
from tests import create_mock_resp_stream, create_pipe_call


class TestWF:  # ===============================================================

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

        mock_resp = create_mock_resp_stream(
            "wf1", should_insert_event_ping=True
        )

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

        mock_resp = create_mock_resp_stream("wf2")

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

        mock_resp = create_mock_resp_stream("wf3")

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

        mock_resp = create_mock_resp_stream("wf4")

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


class TestCF:  # ===============================================================

    def test1(_, testee_cf1):  # BUG
        sr, _ = testee_cf1

        assert next(sr) == "FIRST RESPONSE MESSAGE"
        assert next(sr) == "SECOND RESPONSE MESSAGE"
        assert next(sr) == "THIRD RESPONSE MESSAGE"
