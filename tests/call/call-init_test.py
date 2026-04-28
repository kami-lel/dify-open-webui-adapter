"""
call-init_test.py

Unit Tests (using pytest) for:

OWURequest creation
"""

import pytest

from dify_open_webui_adapter import (
    _PipeCallBody,
    _PipeCallMetadata,
    _PipeCallUser,
)
from tests import create_pipe_call

# Pytest fixtures  #############################################################


@pytest.fixture
def local_call(model_id_wf1):
    model_id = model_id_wf1
    return create_pipe_call(model_id=model_id)


# Pytest unit tests  ###########################################################


class Test1:  # ================================================================

    def test_body(_, local_call):
        opt = local_call
        print(opt)
        assert hasattr(opt, "body")
        assert isinstance(opt.body, _PipeCallBody)

    def test_user(_, local_call):
        opt = local_call
        print(opt)
        assert hasattr(opt, "user")
        assert isinstance(opt.user, _PipeCallUser)

    def test_meta(_, local_call):
        opt = local_call
        print(opt)
        assert hasattr(opt, "metadata")
        assert isinstance(opt.metadata, _PipeCallMetadata)
