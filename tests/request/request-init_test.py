"""
request-init_test.py

Unit Tests (using pytest) for:

OWURequest.__init__()
"""

import pytest

from dify_open_webui_adapter import OWURequest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def request1(pipe_args1):
    args = pipe_args1
    return OWURequest(*args)


# Pytest unit tests  ###########################################################


class Test1:  # ================================================================

    def test_body(_, request1):
        opt = request1
        print(opt)
        assert hasattr(opt, "body")
        assert isinstance(opt.body, dict)

    def test_user(_, request1):
        opt = request1
        print(opt)
        assert hasattr(opt, "user")
        assert isinstance(opt.user, dict)

    def test_meta(_, request1):
        opt = request1
        print(opt)
        assert hasattr(opt, "metadata")
        assert isinstance(opt.metadata, dict)
