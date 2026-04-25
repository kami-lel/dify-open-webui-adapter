"""
call-username_test.py

Unit Tests (using pytest) for:

PipeCall.username
"""

import copy


from dify_open_webui_adapter import PipeCall

# Pytest unit tests  ###########################################################


class TestName:

    def test_dft(_, call_args_empty):
        args = copy.copy(call_args_empty)
        args["user"] = {}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "user"

    def test_only_id(_, call_args_empty):
        ipt = "11223344"
        args = copy.copy(call_args_empty)
        args["user"] = {"id": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_email(_, call_args_empty):
        ipt = "123@gmail"
        args = copy.copy(call_args_empty)
        args["user"] = {"email": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_username(_, call_args_empty):
        ipt = "some user"
        args = copy.copy(call_args_empty)
        args["user"] = {"username": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_name(_, call_args_empty):
        ipt = "some user"
        args = copy.copy(call_args_empty)
        args["user"] = {"name": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_mux1(_, call_args_empty):
        args = copy.copy(call_args_empty)
        args["user"] = {
            "id": "11223344",
            "name": "some user",
            "username": "My Name",
            "email": "123@gmail",
        }

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "some user"

    def test_mux2(_, call_args_empty):
        args = copy.copy(call_args_empty)
        args["user"] = {
            "name": "some user",
            "email": "123@gmail",
        }

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "some user"

    def test_mux3(_, call_args_empty):
        args = copy.copy(call_args_empty)
        args["user"] = {
            "id": "11223344",
            "name": "",
            "email": None,
        }

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "11223344"
