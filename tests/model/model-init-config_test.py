"""
model-init-config_test.py

Unit Tests (using pytest) for:

OWUModel.__init__() related to arg app_model_config
"""


class TestWf1:  # ==============================================================

    def test1(
        _,
    ):
        pass


# TODO TODO

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
