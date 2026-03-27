import pytest

# pytest fixtures  #############################################################


@pytest.fixture
def app_wf_stream(app_wf_skip1):
    app = app_wf_skip1
    app.current_enable_stream = True
    app.current_user_msg_content = "PRIMARY"
    return app


@pytest.fixture
def app_cf_stream(app_cf_skip1):
    app = app_cf_skip1
    app.current_enable_stream = True
    app.current_user_msg_content = "PRIMARY"
    return app


@pytest.fixture
def assertee_wf_stream(endpoint_wf, authorization_wf1):
    assert_args = [endpoint_wf]

    data = (
        '{"inputs": {"query": "PRIMARY"}, '
        '"response_mode": "streaming", '
        '"user": "user"}'
    )

    assert_kwargs = {
        "headers": {
            "Authorization": authorization_wf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": data,
        "stream": True,
        "timeout": 300,
    }
    return assert_args, assert_kwargs


@pytest.fixture
def assertee_cf_stream(endpoint_cf, authorization_cf1):

    data = (
        '{"query": "PRIMARY", '
        '"response_mode": "streaming", '
        '"user": "user", '
        '"conversation_id": "", '
        '"auto_generate_name": false, '
        '"inputs": {}}'
    )

    assert_args = [endpoint_cf]
    assert_kwargs = {
        "headers": {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": data,
        "stream": True,
        "timeout": 300,
    }

    return assert_args, assert_kwargs
