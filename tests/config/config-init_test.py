"""
config-init_test.py

Unit Tests (using pytest) for:

AppModelConfig creation
"""

import copy

from pydantic import ValidationError
import pytest


from dify_open_webui_adapter import AppModelConfig

# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_key(_, config_wf1):
        opt = config_wf1
        print(opt)
        assert hasattr(opt, "key")
        value = opt.key
        assert isinstance(value, str)
        assert len(value) != 0

    def test_model_id(_, config_wf1):
        opt = config_wf1
        print(opt)

        assert hasattr(opt, "model_id")
        value = opt.model_id
        assert isinstance(value, str)
        assert len(value) != 0


# Todo use other configs too


class TestKey:  # ==============================================================

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


class TestId:  # ===============================================================

    def test_miss(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        del raw["model_id"]

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("model_id",)
        assert opt[0]["msg"] == "Field required"

    def test_type(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["model_id"] = 123

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("model_id",)
        assert opt[0]["msg"] == "Input should be a valid string"

    def test_empty(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["model_id"] = ""

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("model_id",)
        assert opt[0]["msg"] == "String should have at least 1 character"
