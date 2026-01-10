"""
conversation_round_test.py

Unit Tests (using pytest) for: _ConversationRound
"""

from .testee_conversation_round import (
    convert_data_dicts_to_lines,
    convert_lines_to_bytes_generator,
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
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(WORKFLOW_DATA1)
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
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(WORKFLOW_DATA2)
        )
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(WORKFLOW_DATA3)
        )
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test4(_):
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(WORKFLOW_DATA4)
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
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(CHATFLOW_DATA1)
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
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(CHATFLOW_DATA2)
        )
        answer = CHATFLOW_ANSWER2

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = convert_lines_to_bytes_generator(
            convert_data_dicts_to_lines(CHATFLOW_DATA3)
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
        lines = convert_data_dicts_to_lines(WORKFLOW_DATA1)
        lines.insert(0, "event: ping")
        text_streams = convert_lines_to_bytes_generator(lines)
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
        lines = convert_data_dicts_to_lines(CHATFLOW_DATA1)
        lines.insert(0, "event: ping")
        text_streams = convert_lines_to_bytes_generator(lines)

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

# BUG write tests for catch errors
