"""
pipe_fx_test.py

Unit Tests (using pytest) for: Pipe.pipe()
"""

import pytest

from tests import EXAMPLE_CONFIGS

from dify_open_webui_adapter import Pipe

# err handle  ##################################################################


class TestBadBody:

    def test_no_msg(_):
        pipe = Pipe(
            app_model_configs_override=EXAMPLE_CONFIGS,
            disable_get_app_type_and_name=True,
        )

        bad_body = {
            "stream": True,
            "messages": [{"role": "user", "content": "FIRST USER MESSAGE"}],
        }

        with pytest.raises(IndexError) as exec_info:
            pipe.pipe(bad_body, None)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "missing entry 'model' in body"
