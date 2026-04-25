"""
pipe-init-models_test.py

Unit Tests (using pytest) for:

Pipe.__init__() populating .models
"""

# Pytest unit tests  ###########################################################


class TestKeys:  # =============================================================

    def test_wf1(_, pipe_obj, model_id_wf1):
        key = model_id_wf1
        opt = pipe_obj.models

        print(opt)
        assert key in opt

    def test_cf1(_, pipe_obj, model_id_cf1):
        key = model_id_cf1
        opt = pipe_obj.models

        print(opt)
        assert key in opt

    def test_cf2(_, pipe_obj, model_id_cf2):
        key = model_id_cf2
        opt = pipe_obj.models

        print(opt)
        assert key in opt


# TODO
