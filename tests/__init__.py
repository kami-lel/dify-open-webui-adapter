import json
from unittest.mock import Mock

from dify_open_webui_adapter import PipeCall


def create_test_call(model_id="default-model-id", stream=False, messages=None):
    messages = messages or [{"role": "user", "content": "Hello Dify"}]

    body = {"model": "dify2owu." + model_id, "messages": messages}
    user = {}
    metadata = {}

    if stream:
        body["stream"] = True

    return PipeCall(body=body, user=user, metadata=metadata)


def create_mock_resp(return_value):
    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = return_value
    return mock_resp


# Hack rm below


def _convert_entries2lines(entries):
    return ["data: " + json.dumps(e) for e in entries]


def _convert_lines2list(entries):
    return [
        ll.encode(encoding="utf-8") for ll in _convert_entries2lines(entries)
    ]


def _convert_entries2iter(entries):
    return iter(_convert_lines2list(entries))
