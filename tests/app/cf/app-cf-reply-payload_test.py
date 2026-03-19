"""
app-cf-reply-payload_test.py

Unit Tests (using pytest) for:

ChatflowApp._create_reply_payload()
"""


class Test1:  # ================================================================

    def test_no_stream(_, app_skip_cf1):
        app = app_skip_cf1
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = False

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"query": "USER MESSAGE", "response_mode": "blocking", '
            '"user": "user", "conversation_id": "", '
            '"auto_generate_name": false, "inputs": {}}'
        )

    def test_stream(_, app_skip_cf1):
        app = app_skip_cf1
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = True

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"query": "USER MESSAGE", "response_mode": "streaming", '
            '"user": "user", "conversation_id": "", '
            '"auto_generate_name": false, "inputs": {}}'
        )
