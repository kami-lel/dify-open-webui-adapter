"""
pipe-init_test.py

Unit Tests (using pytest) for: class Pipe initialization
"""

import pytest

from dify_open_webui_adapter import Pipe


# pytest  ######################################################################
class Test0:  # ================================================================

    def test_container(_, pipe0):
        container = pipe0.model_containers

        print(container)
        assert isinstance(container, dict)
        assert len(container) == 1

    def test_model1(_, pipe0):
        container = pipe0.model_containers

        assert "example-chatflow-model" in container

        opt = container["example-chatflow-model"]
        print(opt)
        assert opt.model_id == "example-chatflow-model"


class Test1:  # ================================================================

    def test_container(_, pipe1):
        container = pipe1.model_containers

        print(container)
        assert isinstance(container, dict)
        assert len(container) == 3

    def test_model1(_, pipe1):
        containers = pipe1.model_containers
        model_id = "example-workflow-model"

        assert model_id in containers
        opt = containers[model_id]
        print(opt)
        assert opt.model_id == model_id

    def test_model2(_, pipe1):
        containers = pipe1.model_containers
        model_id = "example-chatflow-model"

        assert model_id in containers
        opt = containers[model_id]
        print(opt)
        assert opt.model_id == model_id

    def test_model3(_, pipe1):
        containers = pipe1.model_containers
        model_id = "example-chatflow-model-2"

        assert model_id in containers
        opt = containers[model_id]
        print(opt)
        assert opt.model_id == model_id


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
