"""
call-id_test.py

Unit Tests (using pytest) for:

PipeCall.model_id
"""

from tests import create_test_call

# Pytest unit tests  ###########################################################


class TestNormal:  # ===========================================================

    def test_wf1(_, model_id_wf1):
        model_id = model_id_wf1
        call = create_test_call(model_id="dify2owu." + model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf1(_, model_id_cf1):
        model_id = model_id_cf1
        call = create_test_call(model_id="dify2owu." + model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf2(_, model_id_cf2):
        model_id = model_id_cf2
        call = create_test_call(model_id="dify2owu." + model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id


class TestNoPrefix:  # =========================================================

    def test_wf1(_, model_id_wf1):
        model_id = model_id_wf1
        call = create_test_call(model_id=model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf1(_, model_id_cf1):
        model_id = model_id_cf1
        call = create_test_call(model_id=model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf2(_, model_id_cf2):
        model_id = model_id_cf2
        call = create_test_call(model_id=model_id)

        opt = call.model_id
        print(opt)
        assert opt == model_id
