import pytest


# pytest fixtures  #############################################################
# testees  =====================================================================
@pytest.fixture
def testee_wf(app_skip_wf1, patch_target_post):
    app = app_skip_wf1
    app.current_enable_stream = True
    app.current_user_msg_content = "PRIMARY"

    patch_target = patch_target_post

    data = (
        '{"inputs": {"query": "PRIMARY"}, '
        '"response_mode": "streaming", '
        '"user": "user"}'
    )

    assert_args = ["https://api.dify.ai/v1/workflows/run"]
    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": data,
        "stream": True,
        "timeout": 300,
    }

    return app, patch_target, assert_args, assert_kwargs


@pytest.fixture
def testee_cf(app_skip_cf1, patch_target_post):
    app = app_skip_cf1
    app.current_enable_stream = True
    app.current_user_msg_content = "PRIMARY"

    patch_target = patch_target_post

    data = (
        '{"query": "PRIMARY", '
        '"response_mode": "streaming", '
        '"user": "user", '
        '"conversation_id": "", '
        '"auto_generate_name": false, '
        '"inputs": {}}'
    )

    assert_args = ["https://api.dify.ai/v1/chat-messages"]
    assert_kwargs = {
        "headers": {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        "data": data,
        "stream": True,
        "timeout": 300,
    }

    return app, patch_target, assert_args, assert_kwargs
