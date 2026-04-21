"""
call-username_test.py

Unit Tests (using pytest) for:

PipeCall.username
"""

import copy


from dify_open_webui_adapter import PipeCall

# Pytest unit tests  ###########################################################


class TestName:

    def test_dft(_, pipe_args1):
        args = copy.copy(pipe_args1)
        args["user"] = {}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "user"

    def test_only_id(_, pipe_args1):
        ipt = "11223344"
        args = copy.copy(pipe_args1)
        args["user"] = {"id": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_email(_, pipe_args1):
        ipt = "123@gmail"
        args = copy.copy(pipe_args1)
        args["user"] = {"email": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_username(_, pipe_args1):
        ipt = "some user"
        args = copy.copy(pipe_args1)
        args["user"] = {"username": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_only_name(_, pipe_args1):
        ipt = "some user"
        args = copy.copy(pipe_args1)
        args["user"] = {"name": ipt}

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == ipt

    def test_mux1(_, pipe_args1):
        args = copy.copy(pipe_args1)
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

    def test_mux2(_, pipe_args1):
        args = copy.copy(pipe_args1)
        args["user"] = {
            "name": "some user",
            "email": "123@gmail",
        }

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "some user"

    def test_mux3(_, pipe_args1):
        args = copy.copy(pipe_args1)
        args["user"] = {
            "id": "11223344",
            "name": "",
            "email": None,
        }

        call = PipeCall(**args)
        opt = call.username

        print(opt)
        assert opt == "11223344"
