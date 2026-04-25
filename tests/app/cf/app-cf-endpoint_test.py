"""
app-cf-endpoint_test.py

Unit Tests (using pytest) for:

- ChatflowApp._chat_endpoint
"""

# Pytest unit tests  ###########################################################


class Test1:

    def test_cf1(_, app_direct_cf1):
        app = app_direct_cf1

        opt = app._chat_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/chat-messages"

    def test_cf2(_, app_direct_cf2):
        app = app_direct_cf2

        opt = app._chat_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/chat-messages"
