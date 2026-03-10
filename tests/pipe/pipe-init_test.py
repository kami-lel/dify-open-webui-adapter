"""
pipe-init_test.py

Unit Tests (using pytest) for: class Pipe initialization
"""

import pytest

from dify_open_webui_adapter import Pipe


# pytest  ######################################################################
class Test0:  # ================================================================

    pass


class Test1:  # ================================================================
    pass


# HACK HACK make test work

# import pytest

# from dify_open_webui_adapter import Pipe
# from tests import EXAMPLE_CHATFLOW_CONFIG, EXAMPLE_CONFIGS


# def test_verify_app_model_config():
#     config = EXAMPLE_CHATFLOW_CONFIG.copy()
#     del config["model_id"]
#     ipt = [config]

#     with pytest.raises(ValueError):
#         Pipe(ipt)


# class TestContainers:  # test populating self.containers

#     def test1(_):
#         configs = [EXAMPLE_CHATFLOW_CONFIG]
#         pipe = Pipe(
#             app_model_configs_override=configs,
#             disable_get_app_type_and_name=True,
#         )
#         containers = pipe.model_containers

#         print(containers)

#         assert len(containers) == 1

#         # test chatflow container  +++++++++++++++++++++++++++++++++++++++++++++
#         chatflow = containers["example-chatflow-model"]
#         assert chatflow.key == "u0caCsmD"
#         assert chatflow.model_id == "example-chatflow-model"
#         assert chatflow.name == "Example Chatflow Model/App"

#     def test2(_):
#         pipe = Pipe(
#             app_model_configs_override=EXAMPLE_CONFIGS,
#             disable_get_app_type_and_name=True,
#         )
#         containers = pipe.model_containers

#         print(containers)

#         assert len(containers) == 3

#         # test workflow container  +++++++++++++++++++++++++++++++++++++++++++++
#         chatflow = containers["example-workflow-model"]
#         assert chatflow.key == "eaJxetwz"
#         assert chatflow.model_id == "example-workflow-model"
#         assert chatflow.name == "example-workflow-model"

#         # test chatflow container  +++++++++++++++++++++++++++++++++++++++++++++
#         chatflow = containers["example-chatflow-model"]
#         assert chatflow.key == "u0caCsmD"
#         assert chatflow.model_id == "example-chatflow-model"
#         assert chatflow.name == "Example Chatflow Model/App"

#         # test chatflow2 container  ++++++++++++++++++++++++++++++++++++++++++++
#         chatflow = containers["example-chatflow-model-2"]
#         assert chatflow.key == "YIFpPns6"
#         assert chatflow.model_id == "example-chatflow-model-2"
#         assert chatflow.name == "Aux Example Chatflow Model/App"


class TestErr:

    def test_empty(_, base_url):
        ipt = []

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS must contain at least one App/Model"


class TestBadType:  ############################################################

    def test_bad_type1(_, configs1, base_url):
        ipt = configs1.copy()
        ipt.append(123)

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS must contains only dicts: (123,)"

    def test_bad_type2(_, configs1, base_url):
        ipt = configs1.copy()
        ipt.append([1, 2, 3])
        ipt.append("abc")

        with pytest.raises(ValueError) as exec_info:
            Pipe(
                app_model_configs_override=ipt,
                base_url_override=base_url,
                skip_get_app_type_and_name=True,
            )

        msg = str(exec_info.value)
        print(msg)

        assert (
            msg
            == "APP_MODEL_CONFIGS must contains only dicts: ([1, 2, 3], 'abc')"
        )
