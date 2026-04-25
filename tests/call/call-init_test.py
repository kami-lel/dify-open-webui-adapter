"""
call-init_test.py

Unit Tests (using pytest) for:

OWURequest creation
"""

import pytest

from dify_open_webui_adapter import (
    PipeCall,
    _PipeCallBody,
    _PipeCallMetadata,
    _PipeCallUser,
)


# Pytest fixtures  #############################################################
@pytest.fixture
def local_call(call_args_empty):
    return PipeCall(**call_args_empty)


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
