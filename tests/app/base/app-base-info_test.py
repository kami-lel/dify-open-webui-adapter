"""
app-base-info_test.py

Unit Tests (using pytest) for:

BaseDifyApp._info_url
"""


# Pytest unit tests  ###########################################################
class TestInfo:

    def test_wf1(_, app_direct_wf1):
        app = app_direct_wf1

        opt = app._info_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/info"

    def test_cf1(_, app_direct_cf1):
        app = app_direct_cf1

        opt = app._info_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/info"

    def test_cf2(_, app_direct_cf2):
        app = app_direct_cf2

        opt = app._info_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/info"
