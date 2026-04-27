"""
app-base-header_test.py

Unit Tests (using pytest) for:

BaseDifyApp._create_http_header()
"""

from dify_open_webui_adapter import BaseDifyApp


# Pytest unit tests  ###########################################################
class TestHttpHeader:

    def test_no_stream(_, config_wf1, authorization_wf1):
        config = config_wf1

        opt = BaseDifyApp._create_http_header(config, enable_stream=False)
        print(opt)

        assert opt == {
            "Authorization": authorization_wf1,
            "Content-Type": "application/json",
        }

    def test_stream(_, config_cf1, authorization_cf1):
        config = config_cf1

        opt = BaseDifyApp._create_http_header(config, enable_stream=True)
        print(opt)

        assert opt == {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, config_cf2, authorization_cf2):
        config = config_cf2

        opt = BaseDifyApp._create_http_header(config)
        print(opt)

        assert opt == {
            "Authorization": authorization_cf2,
            "Content-Type": "application/json",
        }
