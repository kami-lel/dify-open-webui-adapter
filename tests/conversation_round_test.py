"""
conversation_round_test.py

Unit Tests (using pytest) for: _ConversationRound
"""

from json import JSONDecodeError
import pytest


from .testee_conversation_round import (
    convert_lines_from_data_dicts,
    convert_bytes_generator_from_lines,
    WORKFLOW_DATA1,
    WORKFLOW_DATA2,
    WORKFLOW_DATA3,
    WORKFLOW_DATA4,
    WORKFLOW_ANSWER4,
    CHATFLOW_DATA1,
    CHATFLOW_DATA2,
    CHATFLOW_ANSWER2,
    CHATFLOW_DATA3,
    CHATFLOW_ANSWER3,
)
from dify_open_webui_adapter import _ConversationRound


def _create_simulated_app(text_streams):
    sim_response = type(
        "simulated response",
        (),
        {
            "iter_lines": lambda self: text_streams,
            "close": lambda self: None,
        },
    )()
    sim_app = type(
        "simulated app",
        (),
        {"_open_reply_response": lambda _a, _b: sim_response},
    )
    return sim_app


class TestWorkflow:

    def test1(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(WORKFLOW_DATA1)
        )
        answer = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test2(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(WORKFLOW_DATA2)
        )
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(WORKFLOW_DATA3)
        )
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test4(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(WORKFLOW_DATA4)
        )
        answer = WORKFLOW_ANSWER4

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer


class TestChatflow:
    # BUG test for setting conversation_id

    def test1(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(CHATFLOW_DATA1)
        )
        answer = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test2(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(CHATFLOW_DATA2)
        )
        answer = CHATFLOW_ANSWER2

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(CHATFLOW_DATA3)
        )
        answer = CHATFLOW_ANSWER3

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer


class TestPingEvent:

    def test_workflow(_):
        lines = convert_lines_from_data_dicts(WORKFLOW_DATA1)
        lines.insert(0, "event: ping")
        text_streams = convert_bytes_generator_from_lines(lines)
        answer = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test_chatflow(_):
        lines = convert_lines_from_data_dicts(CHATFLOW_DATA1)
        lines.insert(0, "event: ping")
        text_streams = convert_bytes_generator_from_lines(lines)

        answer = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer


# err handling #################################################################


class TestExhaust:

    def test_workflow1(_):
        data_dicts = WORKFLOW_DATA1[:2]
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(data_dicts)
        )

        with pytest.raises(ValueError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "exhaust text/event-stream "
            "but detect no events indicating finishing"
        )

    def test_chatflow1(_):
        data_dicts = CHATFLOW_DATA1[:2]
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts(data_dicts)
        )

        with pytest.raises(ValueError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "exhaust text/event-stream "
            "but detect no events indicating finishing"
        )


class TestUnicode:

    def test_workflow1(_):
        lines = convert_lines_from_data_dicts(WORKFLOW_DATA1)
        bytes_obj = [bytearray(line, "utf_16") for line in lines]
        text_streams = iter(bytes_obj)

        with pytest.raises(UnicodeDecodeError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )

    def test_chatflow1(_):
        lines = convert_lines_from_data_dicts(CHATFLOW_DATA1)
        bytes_obj = [bytearray(line, "utf_16") for line in lines]
        text_streams = iter(bytes_obj)

        with pytest.raises(UnicodeDecodeError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "fail to decode text/event-stream: "
            "'utf-8' codec can't decode byte 0xff in position 0: "
            "invalid start byte"
        )


class TestJSONDecode:

    def test1(_):
        bad_json = 'data: {"text": "value'
        text_streams = convert_bytes_generator_from_lines([bad_json])

        with pytest.raises(JSONDecodeError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt.startswith("fail to parse text/event-stream as JSON")


class TestKeyErrWorkflow:

    def test_event(_):
        data = {
            "workflow_run_id": "b790",
            "task_id": "04db",
            "data": {
                "text": "FIRST RESPONSE MESSAGE",
                "from_variable_selector": ["4502", "output"],
            },
        }
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""

    def test_data(_):
        data = {
            "event": "text_chunk",
            "workflow_run_id": "b790",
            "task_id": "04db",
        }
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""

    def test_data_text(_):
        data = {
            "event": "text_chunk",
            "workflow_run_id": "b790",
            "task_id": "04db",
            "data": {
                "from_variable_selector": ["4502", "output"],
            },
        }
        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""


class TestKeyErrChatflow:

    def test_event(_):
        data = {
            "conversation_id": "c0cf",
            "message_id": "ff06",
            "created_at": 1768046345,
            "task_id": "5863",
            "id": "ff06",
            "answer": "FIRST RESPONSE MESSAGE",
            "from_variable_selector": ["llm", "text"],
        }

        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""

    def test_answer(_):
        data = {
            "event": "message",
            "conversation_id": "c0cf",
            "message_id": "ff06",
            "created_at": 1768046345,
            "task_id": "5863",
            "id": "ff06",
            "from_variable_selector": ["llm", "text"],
        }

        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""

    def test_conversation_id(_):
        data = {
            "event": "message",
            "message_id": "ff06",
            "created_at": 1768046345,
            "task_id": "5863",
            "id": "ff06",
            "answer": "FIRST RESPONSE MESSAGE",
            "from_variable_selector": ["llm", "text"],
        }

        text_streams = convert_bytes_generator_from_lines(
            convert_lines_from_data_dicts([data])
        )

        with pytest.raises(KeyError) as exec_info:
            for _ in _ConversationRound(
                _create_simulated_app(text_streams), None
            ):
                pass
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""

        # BUG write tests for catch errors
