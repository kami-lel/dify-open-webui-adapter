import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


@pytest.fixture(scope="session")
def model_wf_alt_url(base_url_alt, config_wf1):
    return OWUModel(
        base_url_alt,
        config_wf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def app_wf_alt_url(model_wf_alt_url):
    return model_wf_alt_url.app
