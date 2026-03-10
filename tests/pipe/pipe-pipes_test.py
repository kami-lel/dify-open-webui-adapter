"""
pipe-pipes_test.py

Unit Tests (using pytest) for: Pipe.pipes()
"""

import pytest


# pytest fixtures  #############################################################
@pytest.fixture(scope="session")
def pipe_pipes0(pipe0):
    return pipe0.pipes()


@pytest.fixture(scope="session")
def pipe_pipes1(pipe1):
    return pipe1.pipes()


# pytest  ######################################################################


class Test0:  # ================================================================

    def test_type(_, pipe_pipes0):
        opt = pipe_pipes0

        print(opt)
        assert isinstance(opt, list)
        assert len(opt) == 1

    def test1(_, pipe_pipes0):
        opt = pipe_pipes0[0]

        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "example-chatflow-model",
        }


class Test1:  # ================================================================

    def test_type(_, pipe_pipes1):
        opt = pipe_pipes1

        print(opt)
        assert isinstance(opt, list)
        assert len(opt) == 3

    def test1(_, pipe_pipes1):
        opt = pipe_pipes1[0]

        print(opt)
        assert opt == {
            "id": "example-workflow-model",
            "name": "example-workflow-model",
        }

    def test2(_, pipe_pipes1):
        opt = pipe_pipes1[1]

        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "example-chatflow-model",
        }

    def test3(_, pipe_pipes1):
        opt = pipe_pipes1[2]

        print(opt)
        assert opt == {
            "id": "example-chatflow-model-2",
            "name": "Aux Example Chatflow Model/App",
        }
