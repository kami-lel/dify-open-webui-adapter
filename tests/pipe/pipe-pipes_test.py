"""
pipe-pipes_test.py

Unit Tests (using pytest) for: Pipe.pipes()
"""

from unittest.mock import patch

import pytest

from dify_open_webui_adapter import Pipe

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def pipes_result_single(
    configs_single, patch_target_configs, patch_target_get, mock_sefx_get
):
    configs = configs_single

    with (
        patch(patch_target_configs, configs),
        patch(patch_target_get, side_effect=mock_sefx_get),
    ):
        pipe = Pipe()
        return pipe.pipes()


@pytest.fixture(scope="class")
def pipes_result_mux(pipe_obj):
    return pipe_obj.pipes()


# Pytest unit tests  ###########################################################


class TestSingle:  # ===========================================================

    def test_type(_, pipes_result_single):
        opt = pipes_result_single
        assert isinstance(opt, list)

    def test_len(_, pipes_result_single):
        opt = pipes_result_single
        assert len(opt) == 1

    def test_cf1(_, pipes_result_single):
        opt = pipes_result_single[0]
        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "My Chatflow App",
        }


class TestMux:  # ==============================================================

    def test_type(_, pipes_result_mux):
        opt = pipes_result_mux
        assert isinstance(opt, list)

    def test_len(_, pipes_result_mux):
        opt = pipes_result_mux
        assert len(opt) == 4

    def test_wf1(_, pipes_result_mux):
        opt = pipes_result_mux[0]
        print(opt)
        assert opt == {
            "id": "example-workflow-model",
            "name": "My Workflow App",
        }

    def test_cf1(_, pipes_result_mux):
        opt = pipes_result_mux[2]
        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "My Chatflow App",
        }

    def test_cf2(_, pipes_result_mux):
        opt = pipes_result_mux[3]
        print(opt)
        assert opt == {
            "id": "example-chatflow-model-2",
            "name": "example-chatflow-model-2",
        }
