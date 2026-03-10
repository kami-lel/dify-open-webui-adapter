import sys
from pathlib import Path
import uuid

import pytest

# set up  ######################################################################
# to allows importing from dify_open_webui_adapter.py
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import OWUModel, DifyAppType

# pytest fixtures  #############################################################


# urls  ------------------------------------------------------------------------
@pytest.fixture(scope="session")
def base_url():
    return "https://api.dify.ai/v1"


@pytest.fixture(scope="session")
def base_url_alt():
    return "https://55.44.33.22/v1"


# configs  =====================================================================
@pytest.fixture(scope="session")
def config_wf1():
    return {
        "key": "068937402cc741689986cc5b6ed433a",
        "model_id": "example-workflow-model",
    }


@pytest.fixture(scope="session")
def config_cf1():
    return {
        "key": "f2277b0e16154cba981c866bdc124386",
        "model_id": "example-chatflow-model",
    }


@pytest.fixture(scope="session")
def config_cf2():
    return {
        "key": "820ab10b649b4c748513cb8e7a628063",
        "model_id": "example-chatflow-model-2",
        "name": "Aux Example Chatflow Model/App",
        "disallows_streaming": True,
    }


# model  =======================================================================
@pytest.fixture(scope="session")
def model_skip_wf1(base_url, config_wf1):
    return OWUModel(
        base_url,
        config_wf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.WORKFLOW,
    )


@pytest.fixture(scope="session")
def model_skip_cf1(base_url, config_cf1):
    return OWUModel(
        base_url,
        config_cf1,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


@pytest.fixture(scope="session")
def model_skip_cf2(base_url, config_cf2):
    return OWUModel(
        base_url,
        config_cf2,
        skip_get_app_type_and_name=True,
        app_type_override=DifyAppType.CHATFLOW,
    )


# app  =========================================================================
@pytest.fixture(scope="session")
def app_skip_wf1(model_skip_wf1):
    return model_skip_wf1.app


@pytest.fixture(scope="session")
def app_skip_cf1(model_skip_cf1):
    return model_skip_cf1.app


@pytest.fixture(scope="session")
def app_skip_cf2(model_skip_cf2):
    return model_skip_cf2.app
