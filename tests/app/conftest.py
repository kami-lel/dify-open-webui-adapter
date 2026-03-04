import pytest


from dify_open_webui_adapter import OWUModel


@pytest.fixture
def workflow_model1(base_url, workflow_config1):

    return OWUModel(
        base_url,
        workflow_config1,
        disable_get_app_type_and_name=True,
    )
