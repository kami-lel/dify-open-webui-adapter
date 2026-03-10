"""
http_test.py

Unit Tests (using pytest) for:

create_http_header()
"""

from dify_open_webui_adapter import create_http_header

# pytest fixtures  #############################################################


# tests  #######################################################################
class TestHttpHeader:

    def test_no_stream1(_):
        key = "866bdc1"

        opt = create_http_header(key, enable_stream=False)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 866bdc1",
            "Content-Type": "application/json",
        }

    def test_stream1(_):
        key = "f2277b"

        opt = create_http_header(key, enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
