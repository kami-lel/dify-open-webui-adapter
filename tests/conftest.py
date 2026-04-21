import sys
from pathlib import Path
from unittest.mock import Mock, patch

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

from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
    AppModelConfig,
    WorkflowApp,
    ChatflowApp,
    Pipe,
)

# Hack remove test ignoring
collect_ignore_glob = [
    "app/base/app-base-header_test.py",
    "app/cf/*",
    "app/wf/*",
    "app/app-get_test.py",
    "model/model-reply-last_test.py",
    "pipe/pipe-pipes_test.py",
    "pipe/pipe-pipe_test.py",
    "round/*",
]

# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def pipe_obj(configs_mux, patch_target_configs):
    with patch(patch_target_configs, configs_mux):
        return Pipe()


# patch targets  ---------------------------------------------------------------
@pytest.fixture(scope="session")
def patch_target_get():
    return "dify_open_webui_adapter.requests.get"


@pytest.fixture(scope="session")
def patch_target_post():
    return "dify_open_webui_adapter.requests.post"


@pytest.fixture(scope="session")
def patch_target_configs():
    return "dify_open_webui_adapter.APP_MODEL_CONFIGS"


# app/model configuration  =====================================================

# keys  ------------------------------------------------------------------------


@pytest.fixture(scope="session")
def auth_key_wf1():
    return "068937402cc741689986cc5b6ed433a"


@pytest.fixture(scope="session")
def auth_key_cf1():
    return "f2277b0e16154cba981c866bdc124386"


@pytest.fixture(scope="session")
def auth_key_cf2():
    return "820ab10b649b4c748513cb8e7a628063"


# app names  -------------------------------------------------------------------
@pytest.fixture(scope="session")
def app_given_name_wf1():
    return "My Workflow App"


@pytest.fixture(scope="session")
def app_given_name_cf1():
    return "My Chatflow App"


# raw dicts  -------------------------------------------------------------------


@pytest.fixture(scope="session")
def config_raw_wf1(auth_key_wf1, app_given_name_wf1):
    return {
        "key": auth_key_wf1,
        "model_id": "example-workflow-model",
        "name": app_given_name_wf1,
    }


@pytest.fixture(scope="session")
def config_raw_cf1(auth_key_cf1, app_given_name_cf1):
    return {
        "key": auth_key_cf1,
        "model_id": "example-chatflow-model",
        "name": app_given_name_cf1,
    }


@pytest.fixture(scope="session")
def config_raw_cf2(auth_key_cf2):
    return {
        "key": auth_key_cf2,
        "model_id": "example-chatflow-model-2",
        "disallows_streaming": True,
    }


# config obj  ------------------------------------------------------------------


@pytest.fixture(scope="session")
def config_wf1(config_raw_wf1):
    raw = config_raw_wf1
    return AppModelConfig(**raw)


@pytest.fixture(scope="session")
def config_cf1(config_raw_cf1):
    raw = config_raw_cf1
    return AppModelConfig(**raw)


@pytest.fixture(scope="session")
def config_cf2(config_raw_cf2):
    raw = config_raw_cf2
    return AppModelConfig(**raw)


# config list  -----------------------------------------------------------------


@pytest.fixture(scope="session")
def configs_single(config_raw_cf1):
    return [config_raw_cf1]


@pytest.fixture(scope="session")
def configs_mux(config_raw_wf1, config_raw_cf1, config_raw_cf2):
    return [config_raw_wf1, config_raw_cf1, config_raw_cf2]


# during init  =================================================================


@pytest.fixture
def endpoint_info(base_url):
    return base_url + "/info"


# app names  -------------------------------------------------------------------
@pytest.fixture(scope="session")
def app_response_name_wf1():
    return "Dify Workflow App"


@pytest.fixture(scope="session")
def app_response_name_cf1():
    return "Dify Chatflow App"


# response obj  ----------------------------------------------------------------
@pytest.fixture(scope="class")
def info_response_wf1(app_response_name_wf1):
    return {"mode": "workflow", "name": app_response_name_wf1}


@pytest.fixture(scope="class")
def info_response_cf1(app_response_name_cf1):
    return {"mode": "advanced-chat", "name": app_response_name_cf1}


# mock obj  --------------------------------------------------------------------
@pytest.fixture(scope="class")
def mock_info_wf(info_response_wf1):
    mock_resp = Mock()
    mock_resp.json.return_value = info_response_wf1
    return mock_resp


@pytest.fixture(scope="class")
def mock_info_cf(info_response_cf1):
    mock_resp = Mock()
    mock_resp.json.return_value = info_response_cf1
    return mock_resp


# mock assert  -----------------------------------------------------------------


@pytest.fixture
def mock_assertee_info_wf(endpoint_info, auth_key_wf1):
    args = [endpoint_info]
    kwargs = {
        "headers": {
            "Authorization": "Bearer " + auth_key_wf1,
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }
    return args, kwargs


@pytest.fixture
def mock_assertee_info_cf(endpoint_info, auth_key_cf1):
    args = [endpoint_info]
    kwargs = {
        "headers": {
            "Authorization": "Bearer " + auth_key_cf1,
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }
    return args, kwargs


# directly app  ----------------------------------------------------------------


@pytest.fixture(scope="class")
def app_direct_wf1(config_wf1, info_response_wf1):
    return WorkflowApp(config_wf1, info_response_wf1)


@pytest.fixture(scope="class")
def app_direct_cf1(config_cf1, info_response_cf1):
    return ChatflowApp(config_cf1, info_response_cf1)


@pytest.fixture(scope="class")
def app_direct_cf2(config_cf2):
    return ChatflowApp(config_cf2, {"mode": "advanced-chat"})


# replies  =====================================================================


@pytest.fixture(scope="class")
def pipe_args1():
    body = {}
    user = {}
    metadata = {}
    return {"body": body, "user": user, "metadata": metadata}


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
def endpoint_wf(base_url):
    return base_url + "/workflows/run"


@pytest.fixture
def endpoint_cf(base_url):
    return base_url + "/chat-messages"


# model  =======================================================================
@pytest.fixture()
def model_wf_skip1(base_url, config_raw_wf1):
    return OWUModel(
        base_url,
        config_raw_wf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture()
def model_cf_skip1(base_url, config_raw_cf1):
    return OWUModel(
        base_url,
        config_raw_cf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture()
def model_cf_skip2(base_url, config_raw_cf2):
    return OWUModel(
        base_url,
        config_raw_cf2,
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


# mock  ------------------------------------------------------------------------
@pytest.fixture
def mock_base():
    mock_resp = Mock()
    mock_resp.status_code = 201
    return mock_resp


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
