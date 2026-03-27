import json
from unittest.mock import Mock

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# Pytest fixtures  #############################################################


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
def mock_base():
    mock_resp = Mock()
    mock_resp.status_code = 201
    return mock_resp


@pytest.fixture
def mock_block_wf(mock_base):
    mock_resp = mock_base
    mock_resp.json.return_value = {
        "data": {"outputs": {"answer": "DIFY REPLIED MESSAGE"}}
    }
    return mock_resp


# HACK HACK rm
@pytest.fixture
def patch_reply_no_stream(
    mock_base, patch_target_post, endpoint_wf, authorization_wf1
):

    assert_args = [endpoint_wf]

    assert_kwargs = {
        "headers": {
            "Authorization": authorization_wf1,
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
