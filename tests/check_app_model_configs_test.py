"""
check_non_empty_app_model_configs_test.py

Unit Tests (using pytest) for: _check_app_model_configs_structure()
"""

import pytest

# import verify_app_model_configs  +++++++++++++++++++++++++++++++++++++++++++++

from dify_open_webui_adapter import _check_app_model_configs_structure

from tests import EXAMPLE_CONFIGS


def test_empty():  # when APP_MODEL_CONFIGS is empty
    ipt = []
    msg = None

    with pytest.raises(ValueError) as exec_info:
        _check_app_model_configs_structure(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contains at least one App/Model"


def test_bad_type():
    ipt = EXAMPLE_CONFIGS.copy()
    ipt.append(123)

    msg = None

    with pytest.raises(ValueError) as exec_info:
        _check_app_model_configs_structure(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contains only dicts"
