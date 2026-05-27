import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# set up  ######################################################################
# to allows importing from dify_open_webui_adapter.py
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import (
    AppModelConfig,
    WorkflowApp,
    ChatflowApp,
    Pipe,
)

from tests import (
    convert_key2authorization,
    create_mock_resp_block,
    create_mock_resp_stream,
    load_stream_entries_testee,
)

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def pipe_obj(
    configs_mux, patch_target_configs, patch_target_get, mock_sefx_get
):
    with (
        patch(patch_target_configs, configs_mux),
        patch(patch_target_get, side_effect=mock_sefx_get),
    ):
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


# model ids  -------------------------------------------------------------------


@pytest.fixture(scope="session")
def model_id_wf1():
    return "example-workflow-model"


@pytest.fixture(scope="session")
def model_id_wf2():
    return "workflow-model-changed-input"


@pytest.fixture(scope="session")
def model_id_cf1():
    return "example-chatflow-model"


@pytest.fixture(scope="session")
def model_id_cf2():
    return "example-chatflow-model-2"


# keys  ------------------------------------------------------------------------


@pytest.fixture(scope="session")
def auth_key_wf1():
    return "068937402cc741689986cc5b6ed433a"


@pytest.fixture(scope="session")
def auth_key_wf2():
    return "f1iFcsVcrbuLdVzkgHdq7n8cTUX8gt2c"


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
def config_raw_wf1(auth_key_wf1, app_given_name_wf1, model_id_wf1):
    return {
        "key": auth_key_wf1,
        "model_id": model_id_wf1,
        "name": app_given_name_wf1,
    }


@pytest.fixture(scope="session")
def config_raw_cf1(auth_key_cf1, app_given_name_cf1, model_id_cf1):
    return {
        "key": auth_key_cf1,
        "model_id": model_id_cf1,
        "name": app_given_name_cf1,
    }


@pytest.fixture(scope="session")
def config_raw_cf2(auth_key_cf2, model_id_cf2):
    return {
        "key": auth_key_cf2,
        "model_id": model_id_cf2,
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
def configs_mux(
    config_raw_wf1, config_raw_cf1, config_raw_cf2, auth_key_wf2, model_id_wf2
):
    config_raw_wf2 = {
        "key": auth_key_wf2,
        "model_id": model_id_wf2,
        "query_input_field_identifier": "Input",
        "reply_output_variable_identifier": "Output",
    }
    return [config_raw_wf1, config_raw_wf2, config_raw_cf1, config_raw_cf2]


# during init  =================================================================


@pytest.fixture(scope="session")
def base_url():
    return "https://api.dify.ai/v1"


@pytest.fixture(scope="session")
def endpoint_info(base_url):
    return base_url + "/info"


@pytest.fixture(scope="session")
def chat_endpoint_wf(base_url):
    return base_url + "/workflows/run"


@pytest.fixture(scope="session")
def chat_endpoint_cf(base_url):
    return base_url + "/chat-messages"


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


@pytest.fixture(scope="class")
def info_response_cf2():
    return {"mode": "advanced-chat"}


# mock assert  -----------------------------------------------------------------


@pytest.fixture
def mock_assertee_info_wf(endpoint_info, auth_key_wf1):
    args = [endpoint_info]
    kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_wf1),
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
            "Authorization": convert_key2authorization(auth_key_cf1),
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
def app_direct_cf2(config_cf2, info_response_cf2):
    return ChatflowApp(config_cf2, info_response_cf2)


# mock obj  --------------------------------------------------------------------
@pytest.fixture(scope="class")
def mock_info_wf(info_response_wf1):
    mock_resp = create_mock_resp_block(return_value=info_response_wf1)
    return mock_resp


@pytest.fixture(scope="class")
def mock_info_cf(info_response_cf1):
    mock_resp = create_mock_resp_block(return_value=info_response_cf1)
    return mock_resp


@pytest.fixture(scope="class")
def mock_sefx_get(
    auth_key_wf1,
    auth_key_wf2,
    auth_key_cf1,
    auth_key_cf2,
    mock_info_wf,
    mock_info_cf,
    info_response_cf2,
):
    def get(url, **kwargs):
        key = kwargs["headers"]["Authorization"][7:]

        if key == auth_key_wf1:
            return mock_info_wf
        if key == auth_key_wf2:
            mock_resp = create_mock_resp_block(
                return_value={"mode": "workflow"}
            )
            return mock_resp
        elif key == auth_key_cf1:
            return mock_info_cf
        elif key == auth_key_cf2:
            mock_resp = create_mock_resp_block(return_value=info_response_cf2)
            return mock_resp

        else:
            raise NotImplementedError

    return get


# reply blocking  ==============================================================


@pytest.fixture(scope="class")
def mock_chat_block_wf():
    returned_value = {"data": {"outputs": {"answer": "DIFY REPLIED MESSAGE"}}}
    return create_mock_resp_block(return_value=returned_value)


@pytest.fixture(scope="class")
def mock_assertee_chat_wf_block(chat_endpoint_wf, auth_key_wf1):
    assert_args = [chat_endpoint_wf]

    assert_kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_wf1),
            "Content-Type": "application/json",
        },
        "data": json.dumps({
            "inputs": {"query": "Hello Dify"},
            "response_mode": "blocking",
            "user": "user",
        }),
        "stream": False,
        "timeout": 30,
    }

    return assert_args, assert_kwargs


@pytest.fixture(scope="class")
def mock_chat_block_cf():
    returned_value = {"answer": "DIFY REPLIED MESSAGE"}
    return create_mock_resp_block(return_value=returned_value)


@pytest.fixture(scope="class")
def mock_assertee_chat_cf_block(chat_endpoint_cf, auth_key_cf1):
    assert_args = [chat_endpoint_cf]

    data = {
        "query": "Hello Dify",
        "response_mode": "blocking",
        "user": "user",
        "conversation_id": "",
        "auto_generate_name": False,
        "inputs": {},
    }

    assert_kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_cf1),
            "Content-Type": "application/json",
        },
        "data": json.dumps(data),
        "stream": False,
        "timeout": 30,
    }

    return assert_args, assert_kwargs


# reply streaming  =============================================================


@pytest.fixture(scope="class")
def mock_chat_stream_wf1():
    entries = load_stream_entries_testee("wf1")
    return create_mock_resp_stream(entries)


@pytest.fixture(scope="class")
def mock_assertee_chat_wf_stream(chat_endpoint_wf, auth_key_wf1):
    assert_args = [chat_endpoint_wf]

    assert_kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_wf1),
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps({
            "inputs": {"query": "Hello Dify"},
            "response_mode": "streaming",
            "user": "user",
        }),
        "stream": True,
        "timeout": 300,
    }

    return assert_args, assert_kwargs


@pytest.fixture(scope="class")
def mock_chat_stream_cf1():
    entries = load_stream_entries_testee("cf1")
    return create_mock_resp_stream(entries)


@pytest.fixture(scope="class")
def mock_assertee_chat_cf_stream(chat_endpoint_cf, auth_key_cf1):
    assert_args = [chat_endpoint_cf]

    data = {
        "query": "Hello Dify",
        "response_mode": "streaming",
        "user": "user",
        "conversation_id": "",
        "auto_generate_name": False,
        "inputs": {},
    }

    assert_kwargs = {
        "headers": {
            "Authorization": convert_key2authorization(auth_key_cf1),
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": json.dumps(data),
        "stream": True,
        "timeout": 300,
    }

    return assert_args, assert_kwargs
