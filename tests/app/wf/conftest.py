import json

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType

# Pytest fixtures  #############################################################


@pytest.fixture
def app_changed_input():
    return  # TODO TODO


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
def mock_block_wf(mock_base):
    mock_resp = mock_base
    mock_resp.json.return_value = {
        "data": {"outputs": {"answer": "DIFY REPLIED MESSAGE"}}
    }
    return mock_resp


@pytest.fixture
def assertee_wf_block(endpoint_wf, authorization_wf1):
    args = [endpoint_wf]

    kwargs = {
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

    return args, kwargs
