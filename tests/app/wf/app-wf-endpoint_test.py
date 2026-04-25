"""
app-wf-endpoint_test.py

Unit Tests (using pytest) for:

WorkflowApp._chat_endpoint
"""


# tests  #######################################################################
class Test1:

    def test_wf1(_, app_direct_wf1):
        app = app_direct_wf1

        opt = app._chat_endpoint
        print(opt)
        assert opt == "https://api.dify.ai/v1/workflows/run"
