import json
from unittest.mock import Mock

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture
def testee_block(patch_target_post, endpoint_cf):
    patch_target = patch_target_post

    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {
        "conversation_id": "dc12",
        "answer": "DIFY REPLIED MESSAGE",
    }

    assert_args = [endpoint_cf]

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
