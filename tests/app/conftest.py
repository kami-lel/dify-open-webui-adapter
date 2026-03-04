import pytest


from dify_open_webui_adapter import OWUModel


@pytest.fixture
def wf_model1(base_url, workflow_config1):

    return OWUModel(
        base_url,
        workflow_config1,
        disable_get_app_type_and_name=True,
    )


@pytest.fixture
def cf_model1(base_url, chatflow_config1):

    return OWUModel(
        base_url,
        chatflow_config1,
        disable_get_app_type_and_name=True,
    )


@pytest.fixture
def wf_app1(wf_model1):
    return wf_model1.app


@pytest.fixture
def cf_app1(cf_model1):
    return cf_model1.app
