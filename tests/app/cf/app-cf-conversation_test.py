"""
app-cf-conversation_test.py

Unit Tests (using pytest) for:

ChatflowApp._conversation_id
"""

# Pytest unit tests  ###########################################################


from tests import create_pipe_call


class TestChatId:

    def test_chg_chat_id(_, pipe_obj, model_id_cf1):
        model_id = model_id_cf1
        app = pipe_obj.apps[model_id]
        model = pipe_obj.models[model_id]
        chat_id = "abzca1khdh2ja1q9MYFKRTD5oQwdiIBo"
        model.call = create_pipe_call(
            model_id=model_id, stream=False, chat_id=chat_id
        )

        opt = app._conversation_id

        print(opt)
        assert opt == chat_id
