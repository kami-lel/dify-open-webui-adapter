"""
config-validate_test.py

Unit Tests (using pytest) for:

AppModelConfig.validate_app_model_configs()
"""

from dify_open_webui_adapter import AppModelConfig


# Pytest unit tests  ###########################################################
class TestValidate:

    def test1(_, configs_single):
        configs = configs_single

        print(configs)
        AppModelConfig.validate_app_model_configs(configs)

    def test2(_, configs_mux):
        configs = configs_mux

        print(configs)
        AppModelConfig.validate_app_model_configs(configs)

    # err handling  ------------------------------------------------------------

    # TODO
