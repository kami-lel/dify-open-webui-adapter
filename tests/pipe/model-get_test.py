"""
model-get_test.py

Unit Tests (using pytest) for:

OWUModel.get_model_id_and_name()
"""

# FIXME


class TestGet:

    def test_wf1(_, model_wf_skip1):
        model = model_wf_skip1

        opt = model.get_model_id_and_name()

        print(opt)
        assert opt == {
            "id": "example-workflow-model",
            "name": "example-workflow-model",
        }

    def test_wf2(_, model_wf_provide_name):
        model = model_wf_provide_name

        opt = model.get_model_id_and_name()

        print(opt)
        assert opt == {
            "id": "example-workflow-model",
            "name": "My Workflow Name",
        }

    def test_cf1(_, model_cf_skip1):
        model = model_cf_skip1

        opt = model.get_model_id_and_name()

        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "example-chatflow-model",
        }

    def test_cf2(_, model_cf_provide_name):
        model = model_cf_provide_name

        opt = model.get_model_id_and_name()

        print(opt)
        assert opt == {
            "id": "example-chatflow-model",
            "name": "Example Chatflow Model/App",
        }
