"""
pipe-init_test.py

Unit Tests (using pytest) for: class Pipe initialization
"""

# Pytest unit tests  ###########################################################

# BUG must mock by different functions


class TestPipe:  # =============================================================

    def test_model_type(_, pipe_obj):
        assert isinstance(pipe_obj.models, dict)

    def test_model_size(_, pipe_obj):
        assert len(pipe_obj.models) == 3

    def test_app_type(_, pipe_obj):
        assert isinstance(pipe_obj.apps, dict)

    def test_app_size(_, pipe_obj):
        assert len(pipe_obj.apps) == 3
