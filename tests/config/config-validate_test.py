"""
config-validate_test.py

Unit Tests (using pytest) for:

AppModelConfig.validate_app_model_configs()
"""

import pytest

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

    def test_empty(_):
        configs = []

        with pytest.raises(ValueError) as exec_info:
            AppModelConfig.validate_app_model_configs(configs)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "APP_MODEL_CONFIGS must contain at least one App/Model"

    def test_bad_types(_, configs_mux):
        configs = list(configs_mux)
        # add illegal entry
        configs.append(5)
        configs.append([1, 2, 3])

        with pytest.raises(TypeError) as exec_info:
            AppModelConfig.validate_app_model_configs(configs)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "APP_MODEL_CONFIGS must contains only dicts: 5, [1, 2, 3]"
