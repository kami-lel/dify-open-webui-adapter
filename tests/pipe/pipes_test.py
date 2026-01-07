"""
pipes_test.py

Unit Tests (using pytest) for: Pipe.pipes()
"""

from dify_open_webui_adapter import Pipe
from tests import EXAMPLE_CHATFLOW_CONFIG, EXAMPLE_CONFIGS


class TestPipes:

    def test1(_):
        configs = [EXAMPLE_CHATFLOW_CONFIG]
        pipe = Pipe(
            app_model_configs_override=configs,
            disable_get_app_type_and_name=True,
        )
        opt = pipe.pipes()

        print(opt)

        assert isinstance(opt, list)
        assert len(opt) == 1

        assert opt[0] == {
            "id": "example-chatflow-model",
            "name": "Example Chatflow Model/App",
        }

    def test2(_):
        pipe = Pipe(
            app_model_configs_override=EXAMPLE_CONFIGS,
            disable_get_app_type_and_name=True,
        )
        opt = pipe.pipes()

        print(opt)

        assert isinstance(opt, list)
        assert len(opt) == 3

        assert opt[0] == {
            "id": "example-workflow-model",
            "name": "example-workflow-model",
        }

        assert opt[1] == {
            "id": "example-chatflow-model",
            "name": "Example Chatflow Model/App",
        }

        assert opt[2] == {
            "id": "example-chatflow-model-2",
            "name": "Aux Example Chatflow Model/App",
        }
