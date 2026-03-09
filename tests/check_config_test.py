"""
check_config_test.py

Unit Tests (using pytest) for:

_check_app_model_configs_structure()
"""

import pytest

from dify_open_webui_adapter import _check_app_model_configs_structure


# empty  #######################################################################
def test_empty():
    ipt = []

    with pytest.raises(ValueError) as exec_info:
        _check_app_model_configs_structure(ipt)

    msg = str(exec_info.value)
    print(msg)

    assert msg == "APP_MODEL_CONFIGS must contain at least one App/Model"


class TestBadType:  ############################################################

    def test1(_, configs1):
        ipt = configs1.copy()
        ipt.append(123)

        with pytest.raises(ValueError) as exec_info:
            _check_app_model_configs_structure(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert msg == "APP_MODEL_CONFIGS must contains only dicts: (123,)"

    def test2(_, configs1):
        ipt = configs1.copy()
        ipt.append([1, 2, 3])
        ipt.append("abc")

        with pytest.raises(ValueError) as exec_info:
            _check_app_model_configs_structure(ipt)

        msg = str(exec_info.value)
        print(msg)

        assert (
            msg
            == "APP_MODEL_CONFIGS must contains only dicts: ([1, 2, 3], 'abc')"
        )
