"""
config-stream_test.py

Unit Tests (using pytest) for:

AppModelConfig validation of ``disallows_streaming``
"""

import copy

from pydantic import ValidationError
import pytest


from dify_open_webui_adapter import AppModelConfig


class TestErr:  #  =============================================================

    def test_type(_, config_raw_wf1):
        raw = copy.copy(config_raw_wf1)
        raw["disallows_streaming"] = 123

        with pytest.raises(ValidationError) as exec_info:
            AppModelConfig(**raw)

        opt = exec_info.value.errors()
        print(opt)
        assert len(opt) == 1
        assert opt[0]["loc"] == ("disallows_streaming",)
        assert (
            opt[0]["msg"]
            == "Input should be a valid boolean, unable to interpret input"
        )
