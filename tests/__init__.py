import sys
from pathlib import Path

project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import DifyAppType

EXAMPLE_CHATFLOW_CONFIG = {
    "type": DifyAppType.CHATFLOW,
    "key": "u0caCsmDWe7jRgzxfiU9gBXMXguuPKRp",
    "model_id": "example-chatflow-model",
    "name": "Example Chatflow Model/App",
}
