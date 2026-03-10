"""
app-wf-endpoint_test.py

Unit Tests (using pytest) for:

WorkflowApp.main_url
"""

# tests  #######################################################################


class Test1:

    def test1(_, app_skip_wf1, wf_endpoint):
        opt = app_skip_wf1.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == wf_endpoint

    def test_local1(_, app_wf_alt_url):
        opt = app_wf_alt_url.main_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == "https://55.44.33.22/v1/workflows/run"
