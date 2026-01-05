"""
verify_app_model_configs_test.py

Unit Tests (using pytest) for:

- verify_app_model_configs()
"""

import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++

from dify_open_webui_adapter import verify_app_model_configs

from tests import EXAMPLE_CHATFLOW_CONFIG, EXAMPLE_CONFIGS

# fail cases  ##################################################################


class TestType:

    CONFIG_KEY = "type"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS missing 'type' entry"

    def test_type1(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = "BAD TYPE ENTRY"
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'type' entry must be DifyAppType"

    def test_type2(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'type' entry must be DifyAppType"


# pass cases  ##################################################################


class TestPass:

    def test1(_):
        verify_app_model_configs(EXAMPLE_CONFIGS)
