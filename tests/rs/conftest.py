from unittest.mock import patch


import pytest


from dify_open_webui_adapter import ResponseStream


from tests import create_pipe_call

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_wf1(pipe_obj, model_id_wf1, patch_target_post, mock_chat_stream_wf1):
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_stream_wf1

    with patch(patch_target, return_value=mock_resp) as mock_post:
        sr = ResponseStream(app)

        return sr, mock_post


@pytest.fixture(scope="class")
def testee_cf1(pipe_obj, model_id_cf1, patch_target_post, mock_chat_stream_cf1):
    model_id = model_id_cf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_stream_cf1

    with patch(patch_target, return_value=mock_resp) as mock_post:
        sr = ResponseStream(app)

        return sr, mock_post
