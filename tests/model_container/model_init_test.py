"""
model_init_test.py

Unit Tests (using pytest) for: __init__() of OWUModel
"""

import pytest

from dify_open_webui_adapter import OWUModel, WorkflowDifyApp, ChatflowDifyApp

from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_CHATFLOW2_CONFIG,
    EXAMPLE_WORKFLOW_CONFIG,
)


class TestBaseUrl:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.base_url

        print(opt)
        assert isinstance(opt, str)
        assert opt == EXAMPLE_BASE_URL


class TestKey:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "eaJxetwz"

    def test2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "u0caCsmD"

    def test3(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW2_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.key

        print(opt)
        assert isinstance(opt, str)
        assert opt == "YIFpPns6"


class TestModelId:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-workflow-model"

    def test2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model"

    def test3(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW2_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.model_id

        print(opt)
        assert isinstance(opt, str)
        assert opt == "example-chatflow-model-2"


class TestName:

    def test1(_):
        pass  # TODO


class TestApp:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.app

        print(opt)
        assert isinstance(opt, WorkflowDifyApp)

    def test2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.app

        print(opt)
        assert isinstance(opt, ChatflowDifyApp)
