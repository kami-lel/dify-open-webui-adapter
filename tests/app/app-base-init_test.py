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
def local_workflow_app(workflow_model1):
    return workflow_model1.app


# tests  #######################################################################
class Test1:

    def test_init(_, local_model_app, workflow_model1):
        app = local_model_app
        model = workflow_model1
        assert app.model is model

    def test_base_url(_, local_workflow_app, base_url):
        app = local_workflow_app
        assert app.base_url == base_url
