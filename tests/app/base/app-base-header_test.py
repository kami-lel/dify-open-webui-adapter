"""
app-base-header_test.py

Unit Tests (using pytest) for:

BaseDifyApp.http_header()
"""


class Test1:  # ================================================================

    def test_no_stream(_, app_skip_wf1):
        opt = app_skip_wf1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_stream(_, app_skip_wf1):
        opt = app_skip_wf1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, app_skip_wf1):
        opt = app_skip_wf1.http_header()

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
        }


class Test2:  # ================================================================

    def test_no_stream(_, app_skip_cf1):
        opt = app_skip_cf1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_stream(_, app_skip_cf1):
        opt = app_skip_cf1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, app_skip_cf1):
        opt = app_skip_cf1.http_header()

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
        }
