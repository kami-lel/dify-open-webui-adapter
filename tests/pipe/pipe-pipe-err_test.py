"""
pipe-pipe-err_test.py

Unit Tests (using pytest) for:

errors handling in Pipe.pipe()
"""

import pytest

# Pytest unit tests  ###########################################################


class TestErr:

    @pytest.mark.asyncio
    async def test_no_model(_, pipe_obj, call_args_wf1):
        call_args = call_args_wf1
        body = call_args["body"]
        body["model"] = "aaazzz"
        user = call_args["user"]
        metadata = call_args["metadata"]

        with pytest.raises(ValueError) as exec_info:
            await pipe_obj.pipe(body=body, __user__=user, __metadata__=metadata)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == ""  # BUG
