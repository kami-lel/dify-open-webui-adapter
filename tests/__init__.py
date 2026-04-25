import json

from dify_open_webui_adapter import PipeCall


def create_test_call(model_id="default-model-id", stream=False):
    body = {"model": "dify2owu." + model_id}
    user = {}
    metadata = {}

    if stream:
        body["stream"] = True

    return PipeCall(body=body, user=user, metadata=metadata)


# Hack rm below


def _convert_entries2lines(entries):
    return ["data: " + json.dumps(e) for e in entries]


def _convert_lines2list(entries):
    return [
        ll.encode(encoding="utf-8") for ll in _convert_entries2lines(entries)
    ]


def _convert_entries2iter(entries):
    return iter(_convert_lines2list(entries))
