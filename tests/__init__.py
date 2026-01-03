import sys
from pathlib import Path

project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import DifyAppType

EXAMPLE_WORKFLOW_CONFIG = {
    "type": DifyAppType.WORKFLOW,
    "key": "eaJxetwz",
    "model_id": "example-workflow-model",
}

EXAMPLE_CHATFLOW_CONFIG = {
    "type": DifyAppType.CHATFLOW,
    "key": "u0caCsmD",
    "model_id": "example-chatflow-model",
    "name": "Example Chatflow Model/App",
}

EXAMPLE_CHATFLOW2_CONFIG = {
    "type": DifyAppType.CHATFLOW,
    "key": "YIFpPns6",
    "model_id": "example-chatflow-model-2",
    "name": "Aux Example Chatflow Model/App",
}


EXAMPLE_CONFIGS = [
    EXAMPLE_WORKFLOW_CONFIG,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_CHATFLOW2_CONFIG,
]
