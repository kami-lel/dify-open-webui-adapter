"""
call-username_test.py

Unit Tests (using pytest) for:

PipeCall.username
"""

from tests import create_pipe_call

# Pytest unit tests  ###########################################################


class TestName:

    def test_dft(_, model_id_wf1):
        model_id = model_id_wf1
        user_dict = {}

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)

        opt = call.username

        print(opt)
        assert opt == "user"

    def test_only_id(_, model_id_wf1):
        model_id = model_id_wf1
        ipt = "11223344"
        user_dict = {"id": ipt}

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_email(_, model_id_wf1):
        model_id = model_id_wf1
        ipt = "123@gmail"
        user_dict = {"email": ipt}

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_username(_, model_id_wf1):
        model_id = model_id_wf1
        ipt = "some user"
        user_dict = {"username": ipt}

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_name(_, model_id_wf1):
        model_id = model_id_wf1
        ipt = "some user"
        user_dict = {"name": ipt}

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_mux1(_, model_id_wf1):
        model_id = model_id_wf1
        user_dict = {
            "id": "11223344",
            "name": "some user",
            "username": "My Name",
            "email": "123@gmail",
        }

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == "some user"

    def test_mux2(_, model_id_wf1):
        model_id = model_id_wf1
        user_dict = {
            "name": "some user",
            "email": "123@gmail",
        }

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == "some user"

    def test_mux3(_, model_id_wf1):
        model_id = model_id_wf1
        user_dict = {
            "id": "11223344",
            "name": "",
            "email": None,
        }

        call = create_pipe_call(model_id=model_id, user_dict=user_dict)
        opt = call.username

        print(opt)
        assert opt == "11223344"
