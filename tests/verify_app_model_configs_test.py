"""
verify_app_model_configs_test.py

Unit Tests (using pytest) for:

- verify_app_model_configs()
"""

import pytest
from dify_open_webui_adapter import verify_app_model_configs


def test_empty(_):  # when APP_MODEL_CONFIGS is empty
    ipt = []
    expected_msg = "APP_MODEL_CONFIGS must contains at least one App/Model"
    msg = None

    with pytest.raises(ValueError) as exec_info:
        verify_app_model_configs(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == expected_msg
