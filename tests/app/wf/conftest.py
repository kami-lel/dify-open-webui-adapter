import json

import pytest

from tests import convert_key2authorization

# Pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def chat_endpoint_wf(base_url):
    return base_url + "/workflows/run"


@pytest.fixture
def mock_assertee_block():
    return


# Hack conftest clean up


@pytest.fixture
def mock_block_wf(mock_base):
    mock_resp = mock_base
    mock_resp.json.return_value = {
        "data": {"outputs": {"answer": "DIFY REPLIED MESSAGE"}}
    }
    return mock_resp


@pytest.fixture
def assertee_wf_block(endpoint_wf, auth_key_wf1):
    args = [endpoint_wf]

    kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_wf1),
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
