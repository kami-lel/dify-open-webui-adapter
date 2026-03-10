import pytest


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def model_wf_provide_name(base_url, config_wf1):
    config = config_wf1.copy()
    config["name"] = "My Workflow Name"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def model_cf_provide_name(base_url, config_cf1):
    config = config_cf1.copy()
    config["name"] = "Example Chatflow Model/App"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )
