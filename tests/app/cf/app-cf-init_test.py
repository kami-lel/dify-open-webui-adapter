"""
app-cf-init_test.py

Unit Tests (using pytest) for:

- ChatflowApp.__init__()
"""

# tests  #######################################################################


class Test1:  # ================================================================

    def test_chat_id(_, app_cf_skip1):
        app = app_cf_skip1
        opt = app.current_chat_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == ""

    def test_ids(_, app_cf_skip1):
        app = app_cf_skip1
        opt = app.chat2conversation_ids

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {}
