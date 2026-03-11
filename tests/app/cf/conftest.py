import json
from unittest.mock import Mock

import pytest


@pytest.fixture
def patch_reply_no_stream(patch_target_post, cf_endpoint):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"ok": True}
    mock_resp.text = "APP REPLIED MESSAGE"

    assert_args = [cf_endpoint]

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
        },
        "data": json.dumps({
            "query": "PRIMARY",
            "response_mode": "blocking",
            "user": "user",
            "conversation_id": "",
            "auto_generate_name": False,
            "inputs": {},
        }),
        "stream": False,
        "timeout": 30,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs


@pytest.fixture
def patch_reply_stream(patch_target_post, cf_endpoint):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"ok": True}
    mock_resp.text = "APP REPLIED MESSAGE"

    assert_args = [cf_endpoint]

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps({
            "query": "PRIMARY",
            "response_mode": "streaming",
            "user": "user",
            "conversation_id": "",
            "auto_generate_name": False,
            "inputs": {},
        }),
        "stream": True,
        "timeout": 300,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs
