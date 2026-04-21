"""
app-base-create_header_test.py

Unit Tests (using pytest) for:

BaseDifyApp._create_http_header()
"""

# TODO TODO unit tests


from dify_open_webui_adapter import BaseDifyApp


# Pytest unit tests  ###########################################################
class TestHttpHeader:

    def test_no_stream1(_):
        key = "866bdc1"

        opt = BaseDifyApp._create_http_header(key, enable_stream=False)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 866bdc1",
            "Content-Type": "application/json",
        }

    def test_stream1(_):
        key = "f2277b"

        opt = BaseDifyApp._create_http_header(key, enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
