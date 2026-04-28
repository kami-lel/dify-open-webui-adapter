"""
app-wf-header_test.py

Unit Tests (using pytest) for:

Workflow._http_header (inherited from BaseDifyApp._http_header)
"""

from tests import convert_key2authorization, create_pipe_call

# Pytest unit tests  ###########################################################


class TestWf1:  # ==============================================================

    def test_no_steam(_, pipe_obj, model_id_wf1, auth_key_wf1):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_pipe_call(model_id=model_id, stream=False)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": convert_key2authorization(auth_key_wf1),
            "Content-Type": "application/json",
        }

    def test_steam(_, pipe_obj, model_id_wf1, auth_key_wf1):
        model_id = model_id_wf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_pipe_call(model_id=model_id, stream=True)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": convert_key2authorization(auth_key_wf1),
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
