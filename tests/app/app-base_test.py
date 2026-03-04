"""
app-base_test.py

Unit Tests (using pytest) for BaseDifyApp for:

- .__init__()
- .base_url
- .model_id
- .name
- .http_header()
"""


class Test1:  ##################################################################

    def test_init(_, wf_app1, wf_model1):
        app = wf_app1
        model = wf_model1
        assert app.model is model

    def test_base_url(_, wf_app1, base_url):
        app = wf_app1
        assert app.base_url == base_url

    def test_model_id(_, wf_app1):
        app = wf_app1
        model_id = "example-workflow-model"
        assert app.model_id == model_id

    def test_http_header1(_, wf_app1, wf_model1):
        app = wf_app1
        assert app.http_header(False) == wf_model1.http_header(False)

    def test_http_header2(_, wf_app1, wf_model1):
        app = wf_app1
        assert app.http_header(True) == wf_model1.http_header(True)


class Test2:  ##################################################################

    def test_init(_, cf_app1, cf_model1):
        app = cf_app1
        model = cf_model1
        assert app.model is model

    def test_base_url(_, cf_app1, base_url):
        app = cf_app1
        assert app.base_url == base_url

    def test_model_id(_, cf_app1):
        app = cf_app1
        model_id = "example-chatflow-model"
        assert app.model_id == model_id

    def test_http_header1(_, cf_app1, cf_model1):
        app = cf_app1
        assert app.http_header(False) == cf_model1.http_header(False)

    def test_http_header2(_, cf_app1, cf_model1):
        app = cf_app1
        assert app.http_header(True) == cf_model1.http_header(True)
