"""
model-init-id_test.py

Unit Tests (using pytest) for:

model_id related in OWUModel.__init__()
"""

import pytest

from dify_open_webui_adapter import OWUModel, DifyAppType


# pytest  ######################################################################
class TestModelId:

    def test_wf1(_, wf_model_skip1):
        opt = wf_model_skip1.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-workflow-model"

    def test_cf1(_, cf_model_skip1):
        opt = cf_model_skip1.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model"

    def test_cf2(_, cf_model_skip2):
        opt = cf_model_skip2.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model-2"

    # err handling  ============================================================

    def test_id_present(_, base_url, workflow_config1):
        config = workflow_config1.copy()
        del config["model_id"]

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS missing 'model_id'"

    def test_id_type(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["model_id"] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS must have str 'model_id'"

    def test_id_empty(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["model_id"] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt == "entry in APP_MODEL_CONFIGS must have non-empty 'model_id'"
        )
