"""
check_non_empty_app_model_configs_test.py

Unit Tests (using pytest) for: _check_non_empty_app_model_configs()
"""

import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++

from dify_open_webui_adapter import _check_non_empty_app_model_configs


def test_empty():  # when APP_MODEL_CONFIGS is empty
    ipt = []
    msg = None

    with pytest.raises(ValueError) as exec_info:
        _check_non_empty_app_model_configs(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contains at least one App/Model"
