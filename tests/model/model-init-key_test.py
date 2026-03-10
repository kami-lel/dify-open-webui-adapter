"""
model-init-key_test.py

Unit Tests (using pytest) for:

key-related in OWUModel.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


# pytest  ######################################################################
class TestKey:

    def test_key_present(_, base_url, config_wf1):
        config = config_wf1.copy()
        del config["key"]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS missing 'key'"

    def test_key_type(_, base_url, config_wf1):
        config = config_wf1.copy()

        config["key"] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS must have str 'key'"

    def test_key_empty(_, base_url, config_wf1):
        config = config_wf1.copy()

        config["key"] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'key'"
