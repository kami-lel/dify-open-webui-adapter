"""
config-init-name_test.py

Unit Tests (using pytest) for:

AppModelConfig validation of ``name``
"""

import copy

from pydantic import ValidationError
import pytest


from dify_open_webui_adapter import AppModelConfig


# Pytest unit tests  ###########################################################
class TestId:

    def test_type(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["name"] = 123

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("name",)
        assert opt[0]["msg"] == "Input should be a valid string"

    def test_empty(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["name"] = ""

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("name",)
        assert opt[0]["msg"] == "String should have at least 1 character"
