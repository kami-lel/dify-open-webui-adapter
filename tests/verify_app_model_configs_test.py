"""
verify_app_model_configs_test.py

Unit Tests (using pytest) for:

- verify_app_model_configs()
"""

import sys
from pathlib import Path


import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++
project_root_path = str(Path(__file__).resolve().parents[1])
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from dify_open_webui_adapter import (
    verify_app_model_configs,
)


def test_empty():  # when APP_MODEL_CONFIGS is empty
    ipt = []
    expected_msg = "APP_MODEL_CONFIGS must contains at least one App/Model"
    msg = None

    with pytest.raises(ValueError) as exec_info:
        verify_app_model_configs(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == expected_msg
