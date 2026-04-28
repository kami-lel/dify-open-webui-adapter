"""
pipe-pipe-err_test.py

Unit Tests (using pytest) for:

errors handling in Pipe.pipe()
"""

import pytest

from tests import create_pipe_call_args

# Pytest unit tests  ###########################################################


class TestErr:

    @pytest.mark.asyncio
    async def test_no_model(_, pipe_obj):
        body, user, metadata = create_pipe_call_args()
        body["model"] = "aaazzz"

        with pytest.raises(ValueError) as exec_info:
            await pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "missing model with model_id: aaazzz"
