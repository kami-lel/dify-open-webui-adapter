import pytest

from unittest.mock import Mock

from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def wf_model_skip1(base_url, workflow_config1):
    return OWUModel(
        base_url,
        workflow_config1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def wf_model_skip2(base_url_alt, workflow_config1):
    return OWUModel(
        base_url_alt,
        workflow_config1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def cf_model_skip1(base_url, chatflow_config1):
    return OWUModel(
        base_url,
        chatflow_config1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture(scope="session")
def cf_model_skip2(base_url, chatflow_config2):
    return OWUModel(
        base_url,
        chatflow_config2,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture(scope="session")
def wf_provide_name_model1(base_url, workflow_config1):
    config = workflow_config1.copy()
    config["name"] = "My Workflow Name"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def cf_provide_name_model1(base_url, chatflow_config1):
    config = chatflow_config1.copy()
    config["name"] = "Example Chatflow Model/App"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


# mocks  =======================================================================
@pytest.fixture
def patch_and_result_wf1():
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "mode": "workflow",
        "name": "My Workflow App",
    }

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }

    return mock_resp, assert_kwargs


@pytest.fixture
def patch_and_result_cf1():
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "mode": "advanced-chat",
        "name": "My Chatflow App",
    }

    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
        },
        "timeout": 30,
    }

    return mock_resp, assert_kwargs


@pytest.fixture
def patch_target():
    return "dify_open_webui_adapter.requests.get"


@pytest.fixture
def info_endpoint():
    return "https://api.dify.ai/v1/info"
