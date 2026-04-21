"""
config-init_test.py

Unit Tests (using pytest) for:

AppModelConfig creation
"""

# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_key(_, config_wf1, auth_key_wf1):
        opt = config_wf1
        key_answer = auth_key_wf1

        print(opt)
        assert hasattr(opt, "key")
        value = opt.key
        assert isinstance(value, str)
        assert value == key_answer

    def test_model_id(_, config_wf1):
        opt = config_wf1
        print(opt)

        assert hasattr(opt, "model_id")
        value = opt.model_id
        assert isinstance(value, str)
        assert value == "example-workflow-model"

    def test_name(_, config_wf1, app_given_name_wf1):
        opt = config_wf1
        print(opt)

        assert hasattr(opt, "name")
        value = opt.name
        assert isinstance(value, str)
        assert value == app_given_name_wf1

    def test_stream(_, config_wf1):
        opt = config_wf1
        print(opt)

        assert hasattr(opt, "disallows_streaming")
        value = opt.disallows_streaming
        assert isinstance(value, bool)
        assert not value


class TestCf1:  # ==============================================================

    def test_key(_, config_cf1, auth_key_cf1):
        opt = config_cf1
        key_answer = auth_key_cf1

        print(opt)
        assert hasattr(opt, "key")
        value = opt.key
        assert isinstance(value, str)
        assert value == key_answer

    def test_model_id(_, config_cf1):
        opt = config_cf1
        print(opt)

        assert hasattr(opt, "model_id")
        value = opt.model_id
        assert isinstance(value, str)
        assert value == "example-chatflow-model"

    def test_name(_, config_cf1, app_given_name_cf1):
        opt = config_cf1
        print(opt)

        assert hasattr(opt, "name")
        value = opt.name
        assert isinstance(value, str)
        assert value == app_given_name_cf1

    def test_stream(_, config_cf1):
        opt = config_cf1
        print(opt)

        assert hasattr(opt, "disallows_streaming")
        value = opt.disallows_streaming
        assert isinstance(value, bool)
        assert not value


class TestCf2:  # ==============================================================

    def test_key(_, config_cf2, auth_key_cf2):
        opt = config_cf2
        key_answer = auth_key_cf2

        print(opt)
        assert hasattr(opt, "key")
        value = opt.key
        assert isinstance(value, str)
        assert value == key_answer

    def test_model_id(_, config_cf2):
        opt = config_cf2
        print(opt)

        assert hasattr(opt, "model_id")
        value = opt.model_id
        assert isinstance(value, str)
        assert value == "example-chatflow-model-2"

    def test_name(_, config_cf2):
        opt = config_cf2
        print(opt)

        assert hasattr(opt, "name")
        value = opt.name
        assert value is None

    def test_stream(_, config_cf2):
        opt = config_cf2
        print(opt)

        assert hasattr(opt, "disallows_streaming")
        value = opt.disallows_streaming
        assert isinstance(value, bool)
        assert value
