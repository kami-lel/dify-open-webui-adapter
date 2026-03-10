"""
app-cf-endpoint_test.py

Unit Tests (using pytest) for:

- ChatflowApp.main_url
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType, ChatflowApp

# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def app_cf_alt_url(base_url_alt, config_cf1):
    return ChatflowApp(None, base_url_alt, config_cf1)


# tests  #######################################################################


class Test1:

    def test1(_, app_skip_cf1):
        opt = app_skip_cf1.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://api.dify.ai/v1/chat-messages"

    def test_local1(_, app_cf_alt_url):
        opt = app_cf_alt_url.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://55.44.33.22/v1/chat-messages"
