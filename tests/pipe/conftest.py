import pytest


from dify_open_webui_adapter import Pipe

# Hack pipe fixtures


# pytest fixtures  #############################################################
# pipe object  =================================================================
@pytest.fixture(scope="session")
def pipe0(base_url, configs_single):
    configs = configs_single
    return Pipe(
        app_model_configs_override=configs,
        base_url_override=base_url,
        skip_get_app_type_and_name=True,
    )


@pytest.fixture(scope="session")
def pipe1(base_url, configs_mux):
    configs = configs_mux
    return Pipe(
        app_model_configs_override=configs,
        base_url_override=base_url,
        skip_get_app_type_and_name=True,
    )
