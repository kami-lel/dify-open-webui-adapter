"""
app-cf-header_test.py

Unit Tests (using pytest) for:

Chatflow._http_header (inherited from BaseDifyApp._http_header)
"""

from tests import create_test_call

# Pytest unit tests  ###########################################################


class TestCf1:  # ==============================================================

    def test_no_steam(_, pipe_obj, model_id_cf1, auth_key_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer " + auth_key_cf1,
            "Content-Type": "application/json",
        }

    def test_steam(_, pipe_obj, model_id_cf1, auth_key_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=True)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer " + auth_key_cf1,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }


class TestCf2:  # ==============================================================

    def test_no_steam(_, pipe_obj, model_id_cf2, auth_key_cf2):
        model_id = model_id_cf2
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer " + auth_key_cf2,
            "Content-Type": "application/json",
        }

    def test_steam(_, pipe_obj, model_id_cf2, auth_key_cf2):
        # but not allowed stream in config
        model_id = model_id_cf2
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=True)
        model.call = call

        opt = app._http_header

        print(opt)
        assert opt == {
            "Authorization": "Bearer " + auth_key_cf2,
            "Content-Type": "application/json",
        }
