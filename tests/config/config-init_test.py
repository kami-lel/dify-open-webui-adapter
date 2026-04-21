"""
config-init_test.py

Unit Tests (using pytest) for:

AppModelConfig creation
"""

# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_key(_, config_wf1):
        opt = config_wf1
        print(opt)
        assert hasattr(opt, "key")
        value = opt.key
        assert isinstance(value, str)
        assert len(value) != 0

    def test_model_id(_, config_wf1):
        opt = config_wf1
        print(opt)

        assert hasattr(opt, "model_id")
        value = opt.model_id
        assert isinstance(value, str)
        assert len(value) != 0


# Todo use other configs too
