import sys
from pathlib import Path
import uuid

import pytest


@pytest.fixture(scope="session", autouse=True)
def add_project_root_into_sys_path():
    project_root_path = str(Path(__file__).resolve().parents[1])
    if project_root_path not in sys.path:
        sys.path.insert(0, project_root_path)


@pytest.fixture(scope="session")
def base_url():
    return "https://api.dify.ai/v1"


@pytest.fixture
def random_key():
    return uuid.uuid4.hex


# config  ######################################################################
# workflow config  =============================================================


@pytest.fixture
def workflow_config1(random_key):
    return {
        "key": random_key,
        "model_id": "example-workflow-model",
    }


# chatflow config  =============================================================


@pytest.fixture
def chatflow_config1(random_key):
    return {
        "key": random_key,
        "model_id": "example-chatflow-model",
        "name": "Example Chatflow Model/App",
    }


@pytest.fixture
def chatflow_config2(random_key):
    return {
        "key": random_key,
        "model_id": "example-chatflow-model-2",
        "name": "Aux Example Chatflow Model/App",
    }


# configs  #####################################################################


@pytest.fixture
def configs1(workflow_config1, chatflow_config1, chatflow_config2):
    return [workflow_config1, chatflow_config1, chatflow_config2]
