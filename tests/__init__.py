import json
from unittest.mock import MagicMock, Mock
from pathlib import Path

from dify_open_webui_adapter import PipeCall


def create_pipe_call_args(
    model_id="default-model-id",
    stream=False,
    messages=None,
    user_dict=None,
    chat_id="",
):
    messages = (
        [{"role": "user", "content": "Hello Dify"}]
        if messages is None
        else messages
    )

    body = {"model": "dify2owu." + model_id, "messages": messages}
    user = user_dict or {}
    metadata = {"chat_id": chat_id}

    if stream:
        body["stream"] = True

    return body, user, metadata


def create_pipe_call(*args, **kwargs):
    body, user, metadata = create_pipe_call_args(*args, **kwargs)
    return PipeCall(body=body, user=user, metadata=metadata)


def create_mock_resp_block(return_value):
    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = return_value
    return mock_resp


def convert_key2authorization(key):
    return "Bearer " + key


def load_stream_entries_testee(entry, should_insert_event_ping=False):
    filepath = (
        Path(__file__).parent / "testee" / f"stream_entries_{entry}.json"
    ).resolve()

    with open(filepath, encoding="utf-8") as f:
        entries = json.load(f)  # parse JSON array from file

    lines = ["data: " + json.dumps(e) for e in entries]

    if should_insert_event_ping:
        lines.insert(1, "event: ping")

    encoded = [ll.encode(encoding="utf-8") for ll in lines]

    return encoded


def create_mock_resp_stream(entry, should_insert_event_ping=False):
    mock_resp = MagicMock()
    mock_resp.status_code = 201

    mock_resp.iter_lines.return_value = iter(
        load_stream_entries_testee(
            entry, should_insert_event_ping=should_insert_event_ping
        )
    )
    return mock_resp
