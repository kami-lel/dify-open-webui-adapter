"""
model-init_test.py

Unit Tests (using pytest) for: __init__() of OWUModel
"""


# tests  #######################################################################
class TestBaseUrl:

    def test1(_, base_url, wf_model_skip1):
        model = wf_model_skip1

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test2(_, base_url_alt, wf_model_skip2):
        model = wf_model_skip2

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url_alt

    def test3(_, base_url, cf_model_skip1):
        model = cf_model_skip1

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test4(_, base_url, cf_model_skip2):
        model = cf_model_skip2

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url
