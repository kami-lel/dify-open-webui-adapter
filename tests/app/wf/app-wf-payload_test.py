"""
app-wf-payload_test.py

Unit Tests (using pytest) for:

WorkflowApp._chat_payload
"""

from tests import create_pipe_call


class TestWf1:  # ==============================================================

    def test_no_stream(_, pipe_obj, model_id_wf1):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=False)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"inputs": {"query": "Hello Dify"}, '
            '"response_mode": "blocking", "user": "user"}'
        )

    def test_stream(_, pipe_obj, model_id_wf1):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=True)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"inputs": {"query": "Hello Dify"}, '
            '"response_mode": "streaming", "user": "user"}'
        )


class TestChgIpt:  # ===========================================================

    def test_no_stream(_, pipe_obj, model_id_wf2):
        model_id = model_id_wf2
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=False)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"inputs": {"Input": "Hello Dify"}, '
            '"response_mode": "blocking", "user": "user"}'
        )

    def test_stream(_, pipe_obj, model_id_wf2):
        model_id = model_id_wf2
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        model.call = create_pipe_call(model_id=model_id, stream=True)

        opt = app._chat_payload

        print(opt)
        assert (
            opt
            == '{"inputs": {"Input": "Hello Dify"}, '
            '"response_mode": "streaming", "user": "user"}'
        )
