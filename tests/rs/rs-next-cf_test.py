"""
rs-next-cf_test.py

Unit Tests (using pytest) for:

.__next__() using cf
"""

from unittest.mock import patch

import pytest

from dify_open_webui_adapter import ResponseStream
from tests import create_mock_resp_stream, create_pipe_call

# Pytest unit tests  ###########################################################


class TestNext:

    def test1(_, testee_cf1):
        sr, _ = testee_cf1

        assert next(sr) == "FIRST RESPONSE MESSAGE"
        assert next(sr) == "SECOND RESPONSE MESSAGE"
        assert next(sr) == "THIRD RESPONSE MESSAGE"
        with pytest.raises(StopIteration):
            next(sr)


class TestList:

    def test1(_, testee_cf1):
        sr, _ = testee_cf1

        entries = list(sr)
        print(entries)

        assert entries == [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

    def test1_ping(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        mock_resp = create_mock_resp_stream(
            "cf1", should_insert_event_ping=True
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

    def test2(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        mock_resp = create_mock_resp_stream("cf2")

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)
            assert entries == [
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

    def test3(_, pipe_obj, model_id_cf1, patch_target_post):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        patch_target = patch_target_post

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        mock_resp = create_mock_resp_stream("cf3")

        with patch(patch_target, return_value=mock_resp):
            sr = ResponseStream(app)

            entries = list(sr)
            print(entries)
            assert entries == [
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
