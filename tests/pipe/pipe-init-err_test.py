"""
pipe-init-err_test.py

Unit Tests (using pytest) for:

error handling in Pipe.__init__()
"""

from unittest.mock import patch


from pydantic import ValidationError
import pytest


from dify_open_webui_adapter import Pipe

# Pytest unit tests  ###########################################################


class TestErr:

    def test_empty_config(_, patch_target_configs):
        configs = []
        with patch(patch_target_configs, configs):
            with pytest.raises(Exception) as exec_info:
                Pipe()
            opt = exec_info.value.args[0]

            print(opt)
            assert (
                opt == "APP_MODEL_CONFIGS must contain at least one App/Model"
            )

    def test_bad_config(_, patch_target_configs):
        configs = [{"model_id": "some-random-id"}]
        with patch(patch_target_configs, configs):
            with pytest.raises(ValidationError) as exec_info:
                Pipe()

            opt = exec_info.value.errors()
            print(opt)
            assert len(opt) == 1
            assert opt[0]["loc"] == ("key",)
            assert opt[0]["msg"] == "Field required"
