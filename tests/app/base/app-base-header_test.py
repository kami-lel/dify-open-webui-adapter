"""
app-base-header_test.py

Unit Tests (using pytest) for:

BaseDifyApp.http_header
"""


class Test1:  # ================================================================

    def test_no_stream(_, app_skip_wf1):
        app = app_skip_wf1
        app.current_enable_stream = False
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
        }

    def test_stream(_, app_skip_wf1):
        app = app_skip_wf1
        app.current_enable_stream = True
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }


class Test2:  # ================================================================

    def test_no_stream(_, app_skip_cf1):
        app = app_skip_cf1
        app.current_enable_stream = False
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
        }

    def test_stream(_, app_skip_cf1):
        app = app_skip_cf1
        app.current_enable_stream = True
        opt = app.http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
