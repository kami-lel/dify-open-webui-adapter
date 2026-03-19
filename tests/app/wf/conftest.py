import json
from unittest.mock import Mock

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


@pytest.fixture
def model_changed_input(base_url, config_wf1):
    config = config_wf1.copy()
    config["query_input_field_identifier"] = "Input"
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )
    return model


@pytest.fixture
def app_changed_input(model_changed_input):
    return model_changed_input.app


@pytest.fixture
def patch_reply_no_stream(patch_target_post, wf_endpoint):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {
        "data": {"outputs": {"answer": "DIFY REPLIED MESSAGE"}}
    }

    assert_args = [wf_endpoint]

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
        },
        "data": json.dumps({
            "inputs": {"query": "PRIMARY"},
            "response_mode": "blocking",
            "user": "user",
        }),
        "stream": False,
        "timeout": 30,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs


@pytest.fixture
def patch_reply_stream(patch_target_post, wf_endpoint):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"ok": True}
    mock_resp.text = "APP REPLIED MESSAGE"

    assert_args = [wf_endpoint]

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps({
            "inputs": {"query": "PRIMARY"},
            "response_mode": "streaming",
            "user": "user",
        }),
        "stream": True,
        "timeout": 300,
    }

    return patch_target, mock_resp, assert_args, assert_kwargs
