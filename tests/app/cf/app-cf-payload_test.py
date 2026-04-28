"""
app-cf-payload_test.py

Unit Tests (using pytest) for:

ChatflowApp._chat_payload()
"""

import json

from tests import create_pipe_call


class Test1:  # ================================================================

    def test_no_stream(_, pipe_obj, model_id_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=False)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"query": "Hello Dify", "response_mode": "blocking", '
            '"user": "user", "conversation_id": "", '
            '"auto_generate_name": false, "inputs": {}}'
        )

    def test_stream(_, pipe_obj, model_id_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=True)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"query": "Hello Dify", "response_mode": "streaming", '
            '"user": "user", "conversation_id": "", '
            '"auto_generate_name": false, "inputs": {}}'
        )

    def test_chg_chat_id(_, pipe_obj, model_id_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        chat_id = "abzca1khdh2ja1q9MYFKRTD5oQwdiIBo"
        model.call = create_pipe_call(
            model_id=model_id, stream=False, chat_id=chat_id
        )

        opt = app._chat_payload

        print(opt)
        assert opt == json.dumps({
            "query": "Hello Dify",
            "response_mode": "blocking",
            "user": "user",
            "conversation_id": chat_id,
            "auto_generate_name": False,
            "inputs": {},
        })
