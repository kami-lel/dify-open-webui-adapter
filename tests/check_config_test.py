"""
check_config_test.py

Unit Tests (using pytest) for:

_check_app_model_configs_structure()
"""

import pytest

from dify_open_webui_adapter import _check_app_model_configs_structure


# empty  #######################################################################
def test_empty(empty_configs):
    ipt = empty_configs

    with pytest.raises(ValueError) as exec_info:
        _check_app_model_configs_structure(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contains at least one App/Model"


# TODO more
