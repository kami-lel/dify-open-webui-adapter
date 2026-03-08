"""
model-init_test.py

Unit Tests (using pytest) for: __init__() of OWUModel
"""


# tests  #######################################################################
class TestBaseUrl:

    def test1(_, base_url, wf_model1):
        model = wf_model1

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test2(_, base_url_alt, wf_model2):
        model = wf_model2

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url_alt

    def test3(_, base_url, cf_model1):
        model = cf_model1

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url

    def test4(_, base_url, cf_model2):
        model = cf_model2

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == base_url


# HACK rm
# class TestKey:

#     def test1(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_WORKFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.key

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "eaJxetwz"

#     def test2(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.key

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "u0caCsmD"

#     def test3(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW2_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.key

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "YIFpPns6"


# class TestModelId:

#     def test1(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_WORKFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.model_id

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "example-workflow-model"

#     def test2(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.model_id

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "example-chatflow-model"

#     def test3(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW2_CONFIG,
#             skip_get_app_type_and_name=True,
#         )

#         opt = model.model_id

#         print(opt)
#         assert isinstance(opt, str)
#         assert opt == "example-chatflow-model-2"


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


# class TestApp:

#     def test1(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_WORKFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#             app_type_override=DifyAppType.WORKFLOW,
#         )

#         opt = model.app

#         print(opt)
#         assert isinstance(opt, WorkflowApp)

#     def test2(_):
#         model = OWUModel(
#             EXAMPLE_BASE_URL,
#             EXAMPLE_CHATFLOW_CONFIG,
#             skip_get_app_type_and_name=True,
#             app_type_override=DifyAppType.CHATFLOW,
#         )

#         opt = model.app

#         print(opt)
#         assert isinstance(opt, ChatflowApp)
