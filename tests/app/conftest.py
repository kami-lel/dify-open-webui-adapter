import pytest


from dify_open_webui_adapter import OWUModel, DifyAppType


@pytest.fixture
def wf_model1(base_url, workflow_config1):
    return OWUModel(
        base_url,
        workflow_config1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture
def cf_model1(base_url, chatflow_config1):
    return OWUModel(
        base_url,
        chatflow_config1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture
def cf_model2(base_url, chatflow_config2):
    return OWUModel(
        base_url,
        chatflow_config2,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture
def wf_app1(wf_model1):
    return wf_model1.app


@pytest.fixture
def cf_app1(cf_model1):
    return cf_model1.app


@pytest.fixture
def cf_app2(cf_model2):
    return cf_model2.app
