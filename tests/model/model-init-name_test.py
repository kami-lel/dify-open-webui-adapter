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
def wf_model_provided1(base_url, workflow_config1):
    config = workflow_config1.copy()
    config["name"] = "My Workflow Name"
    return OWUModel(
        base_url,
        config,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


# provided
class TestProvided:  ###########################################################

    def test1(_, wf_model_provided1):
        opt = wf_model_provided1.name

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


# from response  ###############################################################
# TODO TODO

# model id  ####################################################################


# HACK
# class TestName:

#     def test_provided_name1(_):
#         WORKFLOW_NAME = "My Workflow Name"

#         config = EXAMPLE_CHATFLOW_CONFIG.copy()
#         config["name"] = WORKFLOW_NAME

#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             config,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.name

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == WORKFLOW_NAME

#     def test_provided_name2(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.name

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "Example Chatflow Model/App"

#     def test_model_id1(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_WORKFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.name

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "example-workflow-model"

#     def test_model_id2(_):
#         config = EXAMPLE_CHATFLOW_CONFIG.copy()
#         del config["name"]

#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             config,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.name

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "example-chatflow-model"
