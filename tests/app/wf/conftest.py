import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


@pytest.fixture
def model_changed_input(base_url, config_wf1):
    config = config_wf1.copy()
    config["query_input_field_identifier"] = "Input"
    model = OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )
    return model


@pytest.fixture
def app_changed_input(model_changed_input):
    return model_changed_input.app
