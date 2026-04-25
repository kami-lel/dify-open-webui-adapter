"""
app-base-header_test.py

Unit Tests (using pytest) for:

BaseDifyApp.http_header
"""

# Pytest unit tests  ###########################################################


class Test2:  # ================================================================

    def test_no_stream(_, app_cf_skip1, authorization_cf1):
        app = app_cf_skip1
        app.current_enable_stream = False
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
        }

    def test_stream(_, app_cf_skip1, authorization_cf1):
        app = app_cf_skip1
        app.current_enable_stream = True
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": authorization_cf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
