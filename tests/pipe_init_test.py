"""
pipe_init_test.py

Unit Tests (using pytest) for: class Pipe initialization
"""

import pytest

from dify_open_webui_adapter import Pipe
from tests import EXAMPLE_CHATFLOW_CONFIG, EXAMPLE_CONFIGS


def test_verify_app_model_config():
    config = EXAMPLE_CHATFLOW_CONFIG.copy()
    del config["type"]
    ipt = [config]

    with pytest.raises(ValueError):
        Pipe(ipt)


class TestContainers:  # test populating self.containers

    def test1(_):
        configs = [EXAMPLE_CHATFLOW_CONFIG]
        pipe = Pipe(app_model_configs_override=configs)
        containers = pipe.containers

        print(containers)

        assert len(containers) == 1

        # test chatflow container  +++++++++++++++++++++++++++++++++++++++++++++
        chatflow = containers["example-chatflow-model"]
        assert chatflow.key == "u0caCsmD"
        assert chatflow.model_id == "example-chatflow-model"
        assert chatflow.name == "Example Chatflow Model/App"

    def test2(_):
        pipe = Pipe(app_model_configs_override=EXAMPLE_CONFIGS)
        containers = pipe.containers

        print(containers)

        assert len(containers) == 3

        # test workflow container  +++++++++++++++++++++++++++++++++++++++++++++
        chatflow = containers["example-workflow-model"]
        assert chatflow.key == "eaJxetwz"
        assert chatflow.model_id == "example-workflow-model"
        assert chatflow.name is None

        # test chatflow container  +++++++++++++++++++++++++++++++++++++++++++++
        chatflow = containers["example-chatflow-model"]
        assert chatflow.key == "u0caCsmD"
        assert chatflow.model_id == "example-chatflow-model"
        assert chatflow.name == "Example Chatflow Model/App"

        # test chatflow2 container  ++++++++++++++++++++++++++++++++++++++++++++
        chatflow = containers["example-chatflow-model-2"]
        assert chatflow.key == "YIFpPns6"
        assert chatflow.model_id == "example-chatflow-model-2"
        assert chatflow.name == "Aux Example Chatflow Model/App"
