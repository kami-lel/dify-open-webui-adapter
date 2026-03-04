"""
app-base-init_test.py

Unit Tests (using pytest) for BaseDifyApp for:

- .__init__()
- .base_url
- .model_id
- .name
"""

import pytest


# pytest fixture  ##############################################################
@pytest.fixture
def local_wf_app(workflow_model1):
    return workflow_model1.app


# tests  #######################################################################
class Test1:

    def test_init(_, local_wf_app, workflow_model1):
        app = local_wf_app
        model = workflow_model1
        assert app.model is model

    def test_base_url(_, local_wf_app, base_url):
        app = local_wf_app
        assert app.base_url == base_url

    def test_model_id(_, local_wf_app):
        app = local_wf_app
        model_id = "example-workflow-model"
        assert app.model_id == model_id

    def test_http_header1(_, local_wf_app, workflow_model1):
        app = local_wf_app
        assert app.http_header(False) == workflow_model1.http_header(False)

    def test_http_header2(_, local_wf_app, workflow_model1):
        app = local_wf_app
        assert app.http_header(True) == workflow_model1.http_header(True)
