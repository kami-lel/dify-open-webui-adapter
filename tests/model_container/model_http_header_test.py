"""
model_http_header_test.py

Unit Tests (using pytest) for: OWUModel.http_header()
"""

import pytest

from dify_open_webui_adapter import OWUModel

from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_WORKFLOW_CONFIG,
    EXAMPLE_CHATFLOW2_CONFIG,
    EXAMPLE_BODY1,
    EXAMPLE_BODY2,
)


class TestNoStream:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model.http_header(False)

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer u0caCsmD",
            "Content-Type": "application/json",
        }

    def test2(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_WORKFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model.http_header(False)

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer eaJxetwz",
            "Content-Type": "application/json",
        }

    def test3(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW2_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model.http_header(False)

        print(opt)
        assert isinstance(opt, dict)
        assert opt == {
            "Authorization": "Bearer YIFpPns6",
            "Content-Type": "application/json",
        }


class TestStream:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name=True,
        )

        opt = model.http_header(True)

        print(opt)
        assert isinstance(opt, dict)
        assert (
            repr(opt)
            == "{'Authorization': 'Bearer u0caCsmD', "
            "'Content-Type': 'text/event-stream'}"
        )
