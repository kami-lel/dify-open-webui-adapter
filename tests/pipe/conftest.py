import pytest


from dify_open_webui_adapter import Pipe


@pytest.fixture(scope="session")
def pipe0(base_url, configs0):
    configs = configs0
    return Pipe(
        app_model_configs_override=configs,
        base_url_override=base_url,
        skip_get_app_type_and_name=True,
    )


@pytest.fixture(scope="session")
def pipe1(base_url, configs1):
    configs = configs1
    return Pipe(
        app_model_configs_override=configs,
        base_url_override=base_url,
        skip_get_app_type_and_name=True,
    )
