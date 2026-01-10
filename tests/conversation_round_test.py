"""
conversation_round_test.py

Unit Tests (using pytest) for: _ConversationRound
"""

from .testee_conversation_round import (
    WORKFLOW_STREAM1,
    WORKFLOW_STREAM2,
    WORKFLOW_STREAM3,
    WORKFLOW_STREAM4,
    WORKFLOW_ANSWER4,
    CHATFLOW_STREAM1,
    CHATFLOW_STREAM2,
    CHATFLOW_ANSWER2,
    CHATFLOW_STREAM3,
    CHATFLOW_ANSWER3,
    WORKFLOW_PING,
    CHATFLOW_PING,
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
        text_streams = WORKFLOW_STREAM1
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
        text_streams = WORKFLOW_STREAM2
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = WORKFLOW_STREAM3
        answer = ["FIRST RESPONSE MESSAGE"]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test4(_):
        text_streams = WORKFLOW_STREAM4
        answer = WORKFLOW_ANSWER4

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer


class TestChatflow:
    # Bug test for setting conversation_id

    def test1(_):
        text_streams = CHATFLOW_STREAM1
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
        text_streams = CHATFLOW_STREAM2
        answer = CHATFLOW_ANSWER2

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer

    def test3(_):
        text_streams = CHATFLOW_STREAM3
        answer = CHATFLOW_ANSWER3

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(text_streams), None),
            answer,
        ):
            print(opt)
            assert opt == answer


class TestPingEvent:

    def test_workflow(_):
        text_streams = WORKFLOW_PING
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
        text_streams = CHATFLOW_PING
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


# Bug write tests for catch errors
