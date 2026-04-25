"""
model-stream_test.py

Unit Tests (using pytest) for:

OWUModel.is_using_stream
"""

from tests import create_test_call

# Pytest unit tests  ###########################################################


class TestStream:

    def test1(_, pipe_obj, model_id_wf1):
        model_id = model_id_wf1
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=True)
        model.call = call

        opt = model.is_using_stream
        print(opt)
        assert opt

    def test2(_, pipe_obj, model_id_wf1):
        model_id = model_id_wf1
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        opt = model.is_using_stream
        print(opt)
        assert not opt

    def test3(_, pipe_obj, model_id_cf2):
        model_id = model_id_cf2
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=True)
        model.call = call

        opt = model.is_using_stream
        print(opt)
        assert not opt

    def test4(_, pipe_obj, model_id_cf2):
        model_id = model_id_cf2
        model = pipe_obj.models[model_id]

        call = create_test_call(model_id=model_id, stream=False)
        model.call = call

        opt = model.is_using_stream
        print(opt)
        assert not opt
