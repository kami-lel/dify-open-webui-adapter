"""
model_parse_app_model_config_test.py

Unit Tests (using pytest) for: OWUModel._parse_app_model_config_arg()
"""

import pytest

from dify_open_webui_adapter import OWUModel

from tests import EXAMPLE_BASE_URL, EXAMPLE_CHATFLOW_CONFIG


class TestKey:

    CONFIG_KEY = "key"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS missing 'key'"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have str 'key'"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'key'"


class TestModelId:

    CONFIG_KEY = "model_id"

    def test_missing(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS missing 'model_id'"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have str 'model_id'"

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert (
            opt == "entry in APP_MODEL_CONFIGS must have non-empty 'model_id'"
        )


class TestName:
    CONFIG_KEY = "name"

    def test_absent(self):  # no name entry present
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        del config[self.CONFIG_KEY]

        OWUModel(
            EXAMPLE_BASE_URL,
            config,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

    def test_none(self):  # name entry is None
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = None

        OWUModel(
            EXAMPLE_BASE_URL,
            config,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

    def test_empty(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'name'"

    def test_type(self):
        config = EXAMPLE_CHATFLOW_CONFIG.copy()
        config[self.CONFIG_KEY] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                EXAMPLE_BASE_URL,
                config,
                disable_get_app_type_and_name_by_dify_get_info=True,
            )

        opt = str(exec_info.value)
        print(opt)

        assert opt == (
            "entry in APP_MODEL_CONFIGS, "
            + "value of 'name' must be str or None"
        )


# pass cases  ##################################################################
class TestPass:

    def test1(_):
        OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )
