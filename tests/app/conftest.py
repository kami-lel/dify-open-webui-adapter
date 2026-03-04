import pytest


@pytest.fixture
def model1(base_url, workflow_config1):
    # BUG
    from dify_open_webui_adapter import OWUModel

    return OWUModel(
        base_url,
        workflow_config1,
        disable_get_app_type_and_name=True,
    )
