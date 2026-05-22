"""
sr-init_test.py

Unit Tests (using pytest) for:

ResponseStream.__init__()
"""

from unittest.mock import patch


import pytest


from dify_open_webui_adapter import ResponseStream

from tests import create_pipe_call

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def testee_wf(pipe_obj, model_id_wf1, patch_target_post, mock_chat_wf):
    # FIXME make working
    model_id = model_id_wf1
    app = pipe_obj.apps[model_id]
    model = pipe_obj.models[model_id]
    patch_target = patch_target_post

    call = create_pipe_call(model_id=model_id, stream=True)
    model.call = call

    mock_resp = mock_chat_wf

    with patch(patch_target, return_value=mock_resp) as mock_post:
        resp_obj = app.open_chat_response()

        return resp_obj, mock_post


# Pytest unit tests  ###########################################################
class TestWf:  # ==============================================================

    pass


class TestCf:  # ==============================================================
    pass


# TODO
