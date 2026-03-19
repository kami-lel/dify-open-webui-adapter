"""
round-err_test.py

Unit Tests (using pytest) for:

errs handling in _StreamingConversationRound.__next__()
"""

from unittest.mock import patch
from json import JSONDecodeError

import pytest


from dify_open_webui_adapter import _StreamingConversationRound


from tests.round import _convert_lines2list, _convert_entries2lines

# pytest fixtures  #############################################################

# pytest  ######################################################################


class TestExhaust:  # ==========================================================

    def test_wf(_, testee_wf, mock_wf1, stream_entries_wf1):
        app, patch_target, _, _ = testee_wf
        mock_resp = mock_wf1

        lines = _convert_lines2list(stream_entries_wf1)
        lines = lines[:-1]
        mock_resp.iter_lines.return_value = iter(lines)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "exhaust text/event-stream without ending event"

    def test_cf(_, testee_cf, mock_cf1, stream_entries_cf1):
        app, patch_target, _, _ = testee_cf
        mock_resp = mock_cf1

        lines = _convert_lines2list(stream_entries_cf1)
        lines = lines[:-2]
        mock_resp.iter_lines.return_value = iter(lines)

        with pytest.raises(ValueError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "exhaust text/event-stream without ending event"


class TestUnicode:  # ==========================================================

    def test_wf(_, testee_wf, mock_wf1, stream_entries_wf1):
        app, patch_target, _, _ = testee_wf
        mock_resp = mock_wf1

        mock_resp.iter_lines.return_value = iter([
            ll.encode(encoding="utf-16")
            for ll in _convert_entries2lines(stream_entries_wf1)
        ])

        with pytest.raises(UnicodeDecodeError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )

    def test_cf(_, testee_cf, mock_cf1, stream_entries_cf1):
        app, patch_target, _, _ = testee_cf
        mock_resp = mock_cf1

        mock_resp.iter_lines.return_value = iter([
            ll.encode(encoding="utf-16")
            for ll in _convert_entries2lines(stream_entries_cf1)
        ])

        with pytest.raises(UnicodeDecodeError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )


class TestJSONDecode:  # =======================================================

    def test_wf(_, testee_wf, mock_wf1, stream_entries_wf1):
        app, patch_target, _, _ = testee_wf
        mock_resp = mock_wf1

        bad_json = 'data: {"text": "value'

        lines = _convert_lines2list(stream_entries_wf1)
        lines.insert(0, bad_json.encode("utf-8"))
        mock_resp.iter_lines.return_value = iter(lines)

        with pytest.raises(JSONDecodeError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == """fail to parse text/event-stream as JSON: Unterminated string starting at: line 1 column 10 (char 9): b'data: {"text": "value'"""
        )

    def test_cf(_, testee_cf, mock_cf1, stream_entries_cf1):
        app, patch_target, _, _ = testee_cf
        mock_resp = mock_cf1

        bad_json = 'data: {"text": "value'

        lines = _convert_lines2list(stream_entries_cf1)
        lines.insert(0, bad_json.encode("utf-8"))
        mock_resp.iter_lines.return_value = iter(lines)

        with pytest.raises(JSONDecodeError) as exec_info:
            with patch(patch_target, return_value=mock_resp):
                round = _StreamingConversationRound(app)
                list(round)

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == """fail to parse text/event-stream as JSON: Unterminated string starting at: line 1 column 10 (char 9): b'data: {"text": "value'"""
        )


# key err  =====================================================================
class TestKeyErrWorkflow:  # ***************************************************
    pass  # FIXME


#     def test_event(_):
#         data = {
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#             "data": {
#                 "text": "FIRST RESPONSE MESSAGE",
#                 "from_variable_selector": ["4502", "output"],
#             },
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'event'"

#     def test_data(_):
#         data = {
#             "event": "text_chunk",
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'data'"

#     def test_data_text(_):
#         data = {
#             "event": "text_chunk",
#             "workflow_run_id": "b790",
#             "task_id": "04db",
#             "data": {
#                 "from_variable_selector": ["4502", "output"],
#             },
#         }
#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'text'"


class TestKeyErrChatflow:  # ***************************************************
    pass


#     def test_event(_):
#         data = {
#             "conversation_id": "c0cf",
#             "message_id": "ff06",
#             "created_at": 1768046345,
#             "task_id": "5863",
#             "id": "ff06",
#             "answer": "FIRST RESPONSE MESSAGE",
#             "from_variable_selector": ["llm", "text"],
#         }

#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'event'"

#     def test_answer(_):
#         data = {
#             "event": "message",
#             "conversation_id": "c0cf",
#             "message_id": "ff06",
#             "created_at": 1768046345,
#             "task_id": "5863",
#             "id": "ff06",
#             "from_variable_selector": ["llm", "text"],
#         }

#         text_streams = convert_bytes_generator_from_lines(
#             convert_lines_from_data_dicts([data])
#         )

#         with pytest.raises(KeyError) as exec_info:
#             for _ in _StreamingConversationRound(
#                 _create_simulated_app(text_streams), None
#             ):
#                 pass
#         opt = exec_info.value.args[0]

#         print(opt)
#         assert opt == "missing key in text/event-stream content: 'answer'"
