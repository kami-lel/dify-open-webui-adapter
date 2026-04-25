"""
call-id_test.py

Unit Tests (using pytest) for:

PipeCall.model_id
"""

# Pytest unit tests  ###########################################################


class TestNormal:  # ===========================================================

    def test_wf1(_, call_wf1, model_id_wf1):
        call = call_wf1
        model_id = model_id_wf1

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf1(_, call_cf1, model_id_cf1):
        call = call_cf1
        model_id = model_id_cf1

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf2(_, call_cf2, model_id_cf2):
        call = call_cf2
        model_id = model_id_cf2

        opt = call.model_id
        print(opt)
        assert opt == model_id


class TestNoPrefix:  # =========================================================

    def test_wf1(_, call_wf1, model_id_wf1):
        call = call_wf1
        model_id = model_id_wf1
        call.body.model = model_id

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf1(_, call_cf1, model_id_cf1):
        call = call_cf1
        model_id = model_id_cf1
        call.body.model = model_id

        opt = call.model_id
        print(opt)
        assert opt == model_id

    def test_cf2(_, call_cf2, model_id_cf2):
        call = call_cf2
        model_id = model_id_cf2
        call.body.model = model_id

        opt = call.model_id
        print(opt)
        assert opt == model_id
