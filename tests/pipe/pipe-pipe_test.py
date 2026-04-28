"""
pipe-pipe_test.py

Unit Tests (using pytest) for:

Pipe.pipe()
"""

import pytest

# TODO unit test
# Pytest fixtures  #############################################################


@pytest.fixture
def pipe_args_no_stream1(pipe_body1):
    body = pipe_body1
    user = {}
    metadata = {}

    return body, user, metadata


# Pytest unit tests  ###########################################################
class TestErr:  # ==============================================================

    @pytest.mark.asyncio
    async def test_no_model(_, pipe1, pipe_args_no_stream1):
        body, user, metadata = pipe_args_no_stream1
        del body["model"]

        with pytest.raises(IndexError) as exec_info:
            await pipe1.pipe(body, user, metadata)

        opt = exec_info.value.args[0]

        print(opt)
        assert opt == "missing entry 'model' in body"
