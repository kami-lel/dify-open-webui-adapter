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
