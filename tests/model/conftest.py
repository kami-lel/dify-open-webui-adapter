import pytest

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
