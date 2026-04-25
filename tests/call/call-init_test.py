"""
call-init_test.py

Unit Tests (using pytest) for:

OWURequest creation
"""

from dify_open_webui_adapter import (
    _PipeCallBody,
    _PipeCallMetadata,
    _PipeCallUser,
)

# Pytest unit tests  ###########################################################


class Test1:  # ================================================================

    def test_body(_, call_wf1):
        opt = call_wf1
        print(opt)
        assert hasattr(opt, "body")
        assert isinstance(opt.body, _PipeCallBody)

    def test_user(_, call_wf1):
        opt = call_wf1
        print(opt)
        assert hasattr(opt, "user")
        assert isinstance(opt.user, _PipeCallUser)

    def test_meta(_, call_wf1):
        opt = call_wf1
        print(opt)
        assert hasattr(opt, "metadata")
        assert isinstance(opt.metadata, _PipeCallMetadata)
