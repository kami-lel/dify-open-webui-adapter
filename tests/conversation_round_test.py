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

    def test1(_):
        return  # BUG
        TEXT_STREAMS = """data: {"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "FIRST RESPONSE MESSAGE"}},{"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "SECOND RESPONSE MESSAGE"}},{"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "THIRD RESPONSE MESSAGE"}},{"event": "workflow_finished", "task_id": "cbe6", "workflow_run_id": "4085", "data": {}}"""

        answer = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(TEXT_STREAMS), None),
            answer,
        ):
            print(opt)
            assert opt == answer


# Todo more tests for different inputs
# Bug catch errors tests
# Bug test for setting conversation_id
