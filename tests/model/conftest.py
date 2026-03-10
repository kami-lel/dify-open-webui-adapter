import pytest

from unittest.mock import Mock

from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

# pytest fixtures  #############################################################


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
