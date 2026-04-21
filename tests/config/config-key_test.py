"""
config-init-key_test.py

Unit Tests (using pytest) for:

AppModelConfig validation of ``key``
"""

import copy

from pydantic import ValidationError
import pytest


from dify_open_webui_adapter import AppModelConfig


# Pytest unit tests  ###########################################################
class TestKey:

    def test_miss(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        del raw["key"]

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("key",)
        assert opt[0]["msg"] == "Field required"

    def test_type(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["key"] = 123

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("key",)
        assert opt[0]["msg"] == "Input should be a valid string"

    def test_empty(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["key"] = ""

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("key",)
        assert opt[0]["msg"] == "String should have at least 1 character"
