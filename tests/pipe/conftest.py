import pytest


from dify_open_webui_adapter import Pipe


# pytest fixtures  #############################################################
# pipe object  =================================================================
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


# .pipe() args  ================================================================
@pytest.fixture
def pipe_args_no_stream1():
    body = {
        "stream": False,
        "model": "dify_open_webui_adapter.example-chatflow-model",
        "messages": [{"role": "user", "content": "FIRST USER MESSAGE"}],
    }

    user = {}

    metadata = {}

    return body, user, metadata


@pytest.fixture
def pipe_args_stream1(pipe_args_no_stream1):
    body, user, metadata = pipe_args_no_stream1
    body["stream"] = True
    return body, user, metadata


@pytest.fixture
def pipe_args_no_stream2():
    body = {
        "stream": False,
        "model": "dify_open_webui_adapter.example-chatflow-model",
        "messages": [
            {"role": "user", "content": "FIRST USER MESSAGE"},
            {"role": "assistant", "content": "FIRST BOT REPLY"},
            {"role": "user", "content": "SECOND USER MESSAGE"},
            {"role": "assistant", "content": "SECOND BOT REPLY"},
            {"role": "user", "content": "THIRD USER MESSAGE"},
        ],
    }
    user = {}
    metadata = {}
    return body, user, metadata


@pytest.fixture
def pipe_args_stream2(pipe_args_no_stream2):
    body, user, metadata = pipe_args_no_stream2
    body["stream"] = True
    return body, user, metadata
