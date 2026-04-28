"""
app-base-header_test.py

Unit Tests (using pytest) for:

BaseDifyApp._create_http_header()
"""

from dify_open_webui_adapter import BaseDifyApp
from tests import convert_key2authorization


# Pytest unit tests  ###########################################################
class TestHttpHeader:

    def test_no_stream(_, config_wf1, auth_key_wf1):
        config = config_wf1

        opt = BaseDifyApp._create_http_header(config, enable_stream=False)
        print(opt)

        assert opt == {
            "Authorization": convert_key2authorization(auth_key_wf1),
            "Content-Type": "application/json",
        }

    def test_stream(_, config_cf1, auth_key_cf1):
        config = config_cf1

        opt = BaseDifyApp._create_http_header(config, enable_stream=True)
        print(opt)

        assert opt == {
            "Authorization": convert_key2authorization(auth_key_cf1),
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, config_cf2, auth_key_cf2):
        config = config_cf2

        opt = BaseDifyApp._create_http_header(config)
        print(opt)

        assert opt == {
            "Authorization": convert_key2authorization(auth_key_cf2),
            "Content-Type": "application/json",
        }
