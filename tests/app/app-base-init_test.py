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
def local_model_app(model1):
    return model1, model1.app


# tests  #######################################################################
class Test1:

    def test_init(_, local_model_app):
        model, app = local_model_app
        assert app.model is model
