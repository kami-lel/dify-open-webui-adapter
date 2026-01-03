"""
verify_app_model_configs_test.py

Unit Tests (using pytest) for:

- verify_app_model_configs()
"""

import sys
from pathlib import Path


import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import verify_app_model_configs, DifyAppType

EXAMPLE_CHATFLOW_CONFIG = {
    "type": DifyAppType.CHATFLOW,
    "key": "u0caCsmDWe7jRgzxfiU9gBXMXguuPKRp",
    "model_id": "example-chatflow-model",
    "name": "Example Chatflow Model/App",
}

# fail cases  ##################################################################


def test_empty():  # when APP_MODEL_CONFIGS is empty
    ipt = []
    msg = None

    with pytest.raises(ValueError) as exec_info:
        verify_app_model_configs(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contains at least one App/Model"


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


class TestKey:

    CONFIG_KEY = "key"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS missing 'key' entry"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'key' entry must be str"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'key' must not be empty"


class TestModelId:

    CONFIG_KEY = "model_id"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS missing 'model_id' entry"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'model_id' entry must be str"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'model_id' must not be empty"


class TestName:
    CONFIG_KEY = "name"

    def test_absent(self):  # no name entry present
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]
        ipt = [config]

        verify_app_model_configs(ipt)

    def test_none(self):  # name entry is None
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = None
        ipt = [config]

        verify_app_model_configs(ipt)

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""
        ipt = [config]

        with pytest.raises(ValueError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'name' must not be empty"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123
        ipt = [config]

        with pytest.raises(TypeError) as exec_info:
            verify_app_model_configs(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS 'name' entry must be str or None"


# pass cases  ##################################################################

# TODO
