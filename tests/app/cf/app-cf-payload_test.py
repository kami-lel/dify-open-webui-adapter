"""
app-cf-payload_test.py

Unit Tests (using pytest) for:

ChatflowApp._chat_payload()
"""

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
