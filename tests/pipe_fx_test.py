"""
pipe_fx_test.py

Unit Tests (using pytest) for: Pipe.pipe()
"""

import pytest

from tests import EXAMPLE_CONFIGS

from dify_open_webui_adapter import Pipe

# Todo


# err handle  ##################################################################


class TestBadBody:

    def test_no_msg(_):
        pipe = Pipe(app_model_configs=EXAMPLE_CONFIGS)

        bad_body = {
            "stream": True,
            "messages": [{"role": "user", "content": "FIRST USER MESSAGE"}],
        }

        with pytest.raises(IndexError) as exec_info:
            pipe.pipe(bad_body, None)

        opt = str(exec_info.value)
        print(opt)

        assert opt == "missing entry 'model' in body"
