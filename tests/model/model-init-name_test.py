"""
model-init-name_test.py

Unit Tests (using pytest) for: OWUModel.name
"""

from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

import pytest


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def wf_provided_model1(base_url, workflow_config1):
    config = workflow_config1.copy()
    config["name"] = "My Workflow Name"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def cf_no_name_model1(base_url, chatflow_config1):
    config = chatflow_config1.copy()
    del config["name"]
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


# provided
class TestProvided:  ###########################################################

    def test1(_, wf_provided_model1):
        opt = wf_provided_model1.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "My Workflow Name"

    def test2(_, cf_model_skip1):
        opt = cf_model_skip1.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Example Chatflow Model/App"

    def test3(_, cf_model_skip2):
        opt = cf_model_skip2.name

        print(opt)
        assert isinstance(opt, str)
        assert opt == "Aux Example Chatflow Model/App"

    # err handling  ------------------------------------------------------------

    def test_empty_name(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["name"] = ""

        with pytest.raises(ValueError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "entry in APP_MODEL_CONFIGS must have non-empty 'name'"

    def test_bad_type(_, base_url, workflow_config1):
        config = workflow_config1.copy()

        config["name"] = 123

        with pytest.raises(TypeError) as exec_info:
            OWUModel(
                base_url,
                config,
                skip_get_app_type_and_name=True,
                app_type_override=DifyAppType.WORKFLOW,
            )
        opt = exec_info.value.args[0]

        print(opt)
        assert (
            opt
            == "entry in APP_MODEL_CONFIGS, value of 'name' must be str or None"
        )


# from response  ###############################################################
class TestResponse1:

    pass  # TODO


# model id  ####################################################################
