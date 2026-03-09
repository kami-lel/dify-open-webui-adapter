import sys
from pathlib import Path
import uuid

import pytest

# set up  ######################################################################
# to allows importing from dify_open_webui_adapter.py
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)


# pytest fixtures  #############################################################


@pytest.fixture(scope="session")
def base_url():
    return "https://api.dify.ai/v1"


@pytest.fixture(scope="session")
def base_url_alt():
    return "https://55.44.33.22/v1"


# config  ======================================================================
# workflow config  -------------------------------------------------------------


@pytest.fixture(scope="session")
def workflow_config1():
    return {
        "key": "068937402cc741689986cc5b6ed433a",
        "model_id": "example-workflow-model",
    }


# chatflow config  -------------------------------------------------------------


@pytest.fixture(scope="session")
def chatflow_config1():
    return {
        "key": "f2277b0e16154cba981c866bdc124386",
        "model_id": "example-chatflow-model",
    }


@pytest.fixture(scope="session")
def chatflow_config2():
    return {
        "key": "820ab10b649b4c748513cb8e7a628063",
        "model_id": "example-chatflow-model-2",
        "name": "Aux Example Chatflow Model/App",
        "disallows_streaming": True,
    }


# configs  =====================================================================


@pytest.fixture(scope="session")
def configs1(workflow_config1, chatflow_config1, chatflow_config2):
    return [workflow_config1, chatflow_config1, chatflow_config2]
