"""
model-init-config_test.py

Unit Tests (using pytest) for:

OWUModel.__init__() related to arg app_model_skip_config
"""


class TestWf1:  # ==============================================================

    def test_key(_, wf_model_skip1, workflow_config1):
        opt = wf_model_skip1.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == workflow_config1["key"]

    def test_model(_, wf_model_skip1):
        opt = wf_model_skip1.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-workflow-model"

    def test_disallow(_, wf_model_skip1):
        opt = wf_model_skip1.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


class TestCf1:  # ==============================================================

    def test_key(_, cf_model_skip1, chatflow_config1):
        opt = cf_model_skip1.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == chatflow_config1["key"]

    def test_model(_, cf_model_skip1):
        opt = cf_model_skip1.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model"

    def test_disallow(_, cf_model_skip1):
        opt = cf_model_skip1.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert not opt


class TestCf2:  # ==============================================================

    def test_key(_, cf_model_skip2, chatflow_config2):
        opt = cf_model_skip2.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == chatflow_config2["key"]

    def test_model(_, cf_model_skip2):
        opt = cf_model_skip2.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model-2"

    def test_disallow(_, cf_model_skip2):
        opt = cf_model_skip2.disallows_streaming

        print(opt)
        assert isinstance(opt, bool)
        assert opt
