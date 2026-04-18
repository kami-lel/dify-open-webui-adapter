import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from tests import (
    _convert_entries2iter,
    STREAM_ENTRIES_WF1,
    STREAM_ENTRIES_WF2,
    STREAM_ENTRIES_WF3,
    STREAM_ENTRIES_WF4,
    STREAM_ENTRIES_CF1,
    STREAM_ENTRIES_CF2,
    STREAM_ENTRIES_CF3,
)

# set up  ######################################################################
# to allows importing from dify_open_webui_adapter.py
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


# Hack rm below  ###############################################################


# base urls  -------------------------------------------------------------------
@pytest.fixture(scope="session")
def base_url():
    return "https://api.dify.ai/v1"


@pytest.fixture(scope="session")
def base_url2():
    return "https://55.44.33.22/v1"


# endpoints  -------------------------------------------------------------------
@pytest.fixture
def endpoint_info(base_url):
    return base_url + "/info"


@pytest.fixture
def endpoint_wf(base_url):
    return base_url + "/workflows/run"


@pytest.fixture
def endpoint_cf(base_url):
    return base_url + "/chat-messages"


# configurations  ==============================================================


@pytest.fixture(scope="session")
def auth_key_wf1():
    return "068937402cc741689986cc5b6ed433a"


@pytest.fixture(scope="session")
def auth_key_cf1():
    return "f2277b0e16154cba981c866bdc124386"


@pytest.fixture(scope="session")
def authorization_wf1(auth_key_wf1):
    return "Bearer " + auth_key_wf1


@pytest.fixture(scope="session")
def authorization_cf1(auth_key_cf1):
    return "Bearer " + auth_key_cf1


# config  ----------------------------------------------------------------------
@pytest.fixture(scope="session")
def config_wf1(auth_key_wf1):
    return {
        "key": auth_key_wf1,
        "model_id": "example-workflow-model",
    }


@pytest.fixture(scope="session")
def config_cf1(auth_key_cf1):
    return {
        "key": auth_key_cf1,
        "model_id": "example-chatflow-model",
    }


@pytest.fixture(scope="session")
def config_cf2():
    return {
        "key": "820ab10b649b4c748513cb8e7a628063",
        "model_id": "example-chatflow-model-2",
        "name": "Aux Example Chatflow Model/App",
        "disallows_streaming": True,
    }


# configs  ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def configs_single(config_cf1):
    return [config_cf1]


@pytest.fixture(scope="session")
def configs_mux(config_wf1, config_cf1, config_cf2):
    return [config_wf1, config_cf1, config_cf2]


# model  =======================================================================
@pytest.fixture()
def model_wf_skip1(base_url, config_wf1):
    return OWUModel(
        base_url,
        config_wf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture()
def model_cf_skip1(base_url, config_cf1):
    return OWUModel(
        base_url,
        config_cf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture()
def model_cf_skip2(base_url, config_cf2):
    return OWUModel(
        base_url,
        config_cf2,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


# app  =========================================================================
@pytest.fixture()
def app_wf_skip1(model_wf_skip1):
    return model_wf_skip1.app


@pytest.fixture()
def app_cf_skip1(model_cf_skip1):
    return model_cf_skip1.app


@pytest.fixture()
def app_cf_skip2(model_cf_skip2):
    return model_cf_skip2.app


# mocks  =======================================================================

# patch targets  ---------------------------------------------------------------


@pytest.fixture
def patch_target_get():
    return "dify_open_webui_adapter.requests.get"


@pytest.fixture
def patch_target_post():
    return "dify_open_webui_adapter.requests.post"


# mock  ------------------------------------------------------------------------
@pytest.fixture
def mock_base():
    mock_resp = Mock()
    mock_resp.status_code = 201
    return mock_resp


# info tests  ==================================================================


@pytest.fixture
def mock_info_wf():
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "mode": "workflow",
        "name": "My Workflow App",
    }
    return mock_resp


@pytest.fixture
def mock_info_cf():
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "mode": "advanced-chat",
        "name": "My Chatflow App",
    }
    return mock_resp


@pytest.fixture
def assertee_info_wf(endpoint_info, authorization_wf1):
    args = [endpoint_info]
    kwargs = {
        "headers": {
            "Authorization": authorization_wf1,
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }
    return args, kwargs


@pytest.fixture
def assertee_info_cf(endpoint_info, authorization_cf1):
    args = [endpoint_info]
    kwargs = {
        "headers": {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }
    return args, kwargs


# streaming  ===================================================================


# stream entries  --------------------------------------------------------------
@pytest.fixture
def stream_entries_wf1():
    return STREAM_ENTRIES_WF1


@pytest.fixture
def stream_entries_cf1():
    return STREAM_ENTRIES_CF1


# wf mocks  --------------------------------------------------------------------


@pytest.fixture
def mock_wf1(mock_base, stream_entries_wf1):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        stream_entries_wf1
    )
    return mock_resp


@pytest.fixture
def mock_wf2(mock_base):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        STREAM_ENTRIES_WF2
    )

    return mock_resp


@pytest.fixture
def mock_wf3(mock_base):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        STREAM_ENTRIES_WF3
    )
    return mock_resp


@pytest.fixture
def mock_wf4(mock_base):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        STREAM_ENTRIES_WF4
    )
    return mock_resp


# cf mocks  --------------------------------------------------------------------


@pytest.fixture
def mock_cf1(mock_base, stream_entries_cf1):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        stream_entries_cf1
    )
    return mock_resp


@pytest.fixture
def mock_cf2(mock_base):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        STREAM_ENTRIES_CF2
    )
    return mock_resp


@pytest.fixture
def mock_cf3(mock_base):
    mock_resp = mock_base
    mock_resp.iter_lines.return_value = _convert_entries2iter(
        STREAM_ENTRIES_CF3
    )
    return mock_resp


# .pipe() args  ================================================================

# Hack pipe fixtures


@pytest.fixture
def pipe_body1():
    return {
        "stream": False,
        "model": "dify_open_webui_adapter.example-chatflow-model",
        "messages": [{"role": "user", "content": "FIRST USER MESSAGE"}],
    }


@pytest.fixture
def pipe_args_stream1(pipe_body1, pipe_args_no_stream1):
    _, user, metadata = pipe_args_no_stream1
    body = pipe_body1
    body["stream"] = True
    return body, user, metadata


@pytest.fixture
def pipe_args_no_stream2(pipe_body2):
    body = pipe_body2
    user = {}
    metadata = {}
    return body, user, metadata


def pipe_args_stream2(pipe_body2, pipe_args_no_stream2):
    _, user, metadata = pipe_args_no_stream2
    body = pipe_body2
    body["stream"] = True
    return body, user, metadata
