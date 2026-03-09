"""
model-header_test.py

Unit Tests (using pytest) for: OWUModel.http_header()
"""


class Test1:  # ================================================================

    def test_no_stream(_, wf_model_skip1):
        opt = wf_model_skip1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_stream(_, wf_model_skip1):
        opt = wf_model_skip1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, wf_model_skip1):
        opt = wf_model_skip1.http_header()

        print(opt)
        assert opt == {
            "Authorization": "Bearer 068937402cc741689986cc5b6ed433a",
            "Content-Type": "application/json",
        }


class Test2:  # ================================================================

    def test_no_stream(_, cf_model_skip1):
        opt = cf_model_skip1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_stream(_, cf_model_skip1):
        opt = cf_model_skip1.http_header(enable_stream=True)

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def test_dft(_, cf_model_skip1):
        opt = cf_model_skip1.http_header()

        print(opt)
        assert opt == {
            "Authorization": "Bearer f2277b0e16154cba981c866bdc124386",
            "Content-Type": "application/json",
        }
