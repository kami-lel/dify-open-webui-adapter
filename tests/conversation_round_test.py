"""
conversation_round_test.py

Unit Tests (using pytest) for: _ConversationRound
"""

from dify_open_webui_adapter import _ConversationRound


def _create_simulated_app(text_streams):
    iter_lines = iter([v.encode("utf-8") for v in text_streams.split("\n")])
    sim_response = type(
        "simulated response",
        (),
        {
            "iter_lines": lambda self: iter_lines,
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
        TEXT_STREAMS = """data: {"event": "message", "task_id": "cbe6", "message_id": "4085", "conversation_id": "7691", "answer": "FIRST RESPONSE MESSAGE", "created_at": 1705395332}
data: {"event": "message", "task_id": "cbe6", "message_id": "4085", "conversation_id": "7691", "answer": "SECOND RESPONSE MESSAGE", "created_at": 1705395332}
data: {"event": "message", "task_id": "cbe6", "message_id": "4085", "conversation_id": "7691", "answer": "THIRD RESPONSE MESSAGE", "created_at": 1705395332}
data: {"event": "message_end", "task_id": "cbe6", "message_id": "4085", "conversation_id": "7691", "metadata": {}}"""

        ANSWER = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(TEXT_STREAMS), None),
            ANSWER,
        ):
            print(opt)
            assert opt == answer


class TestChatflow:

    def test1(_):
        TEXT_STREAMS = """data: {"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "FIRST RESPONSE MESSAGE"}}
data: {"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "SECOND RESPONSE MESSAGE"}}
data: {"event": "text_chunk", "task_id": "cbe6", "workflow_run_id": "4085", "data": {"text": "THIRD RESPONSE MESSAGE"}}
data: {"event": "workflow_finished", "task_id": "cbe6", "workflow_run_id": "4085", "data": {}}"""

        ANSWER = [
            "FIRST RESPONSE MESSAGE",
            "SECOND RESPONSE MESSAGE",
            "THIRD RESPONSE MESSAGE",
        ]

        for opt, answer in zip(
            _ConversationRound(_create_simulated_app(TEXT_STREAMS), None),
            ANSWER,
        ):
            print(opt)
            assert opt == answer


# Todo more tests for different inputs
# Bug catch errors tests
# Bug test for setting conversation_id
