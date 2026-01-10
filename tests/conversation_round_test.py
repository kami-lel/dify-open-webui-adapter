"""
conversation_round_test.py

Unit Tests (using pytest) for: _ConversationRound
"""

from dify_open_webui_adapter import _ConversationRound


def test_1():
    # workflow test
    # TODO

    TEXT_STREAMS = [
        'data: {"event": "text_chunk", "task_id": "cbe6", "workflow_run_id":'
        ' "4085", "event": "text_chunk", "data": {"text": "FIRST RESPONSE'
        ' MESSAGE"}}'
    ]
    ANSWER = ["FIRST RESPONSE MESSAGE"]

    app = None
    iter_lines = iter([v.encode("utf-8") for v in TEXT_STREAMS])

    for opt, answer in zip(
        _ConversationRound(app, None, iter_lines_override=iter_lines),
        ANSWER,
    ):
        print(opt)
        assert opt == answer
