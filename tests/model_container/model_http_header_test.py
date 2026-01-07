"""
model_http_header_test.py

Unit Tests (using pytest) for: OWUModel.http_header()
"""

import pytest

from dify_open_webui_adapter import OWUModel

from tests import (
    EXAMPLE_BASE_URL,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_BODY1,
    EXAMPLE_BODY2,
)


class TestNoStream:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.http_header(False)

        print(opt)
        assert isinstance(opt, dict)
        assert (
            repr(opt)
            == "{'Authorization': 'Bearer u0caCsmD', "
            "'Content-Type': 'application/json'}"
        )


class TestStream:

    def test1(_):
        model = OWUModel(
            EXAMPLE_BASE_URL,
            EXAMPLE_CHATFLOW_CONFIG,
            disable_get_app_type_and_name_by_dify_get_info=True,
        )

        opt = model.http_header(True)

        print(opt)
        assert isinstance(opt, dict)
        assert (
            repr(opt)
            == "{'Authorization': 'Bearer u0caCsmD', "
            "'Content-Type': 'text/event-stream'}"
        )
