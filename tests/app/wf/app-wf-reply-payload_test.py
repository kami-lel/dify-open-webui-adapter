"""
app-wf-reply-payload_test.py

Unit Tests (using pytest) for:

WorkflowApp._create_reply_payload()
"""


class Test1:  # ================================================================

    def test_no_stream(_, app_skip_wf1):
        app = app_skip_wf1
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = False

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"inputs": {"query": "USER MESSAGE"}, '
            '"response_mode": "blocking", "user": "user"}'
        )

    def test_stream(_, app_skip_wf1):
        app = app_skip_wf1
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = True

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"inputs": {"query": "USER MESSAGE"}, '
            '"response_mode": "streaming", "user": "user"}'
        )


class Test2:  # ================================================================

    def test_no_stream(_, app_changed_input):
        app = app_changed_input
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = False

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"inputs": {"Input": "USER MESSAGE"}, '
            '"response_mode": "blocking", "user": "user"}'
        )

    def test_stream(_, app_changed_input):
        app = app_changed_input
        app.current_user_msg_content = "USER MESSAGE"
        app.current_enable_stream = True

        opt = app._create_reply_payload()

        print(opt)
        assert (
            opt
            == '{"inputs": {"Input": "USER MESSAGE"}, '
            '"response_mode": "streaming", "user": "user"}'
        )
