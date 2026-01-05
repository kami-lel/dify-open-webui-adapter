"""
model_parse_app_model_config_test.py

Unit Tests (using pytest) for: OWUModel._parse_app_model_config_arg()
"""

import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++

from dify_open_webui_adapter import OWUModel

from tests import EXAMPLE_BASE_URL, EXAMPLE_CHATFLOW_CONFIG, EXAMPLE_CONFIGS


class TestKey:

    CONFIG_KEY = "key"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS missing 'key'"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have str 'key'"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'key'"


class TestModelId:

    CONFIG_KEY = "model_id"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "APP_MODEL_CONFIGS missing 'model_id' entry"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "APP_MODEL_CONFIGS 'model_id' entry must be str"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "APP_MODEL_CONFIGS 'model_id' must not be empty"


class TestName:
    CONFIG_KEY = "name"

    def test_absent(self):  # no name entry present
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        OWUModel(EXAMPLE_BASE_URL, ipt)

    def test_none(self):  # name entry is None
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = None
        ipt = [config]

        OWUModel(EXAMPLE_BASE_URL, ipt)

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "APP_MODEL_CONFIGS 'name' must not be empty"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            OWUModel(EXAMPLE_BASE_URL, ipt)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "APP_MODEL_CONFIGS 'name' entry must be str or None"
