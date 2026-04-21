"""
model-init-name_test.py

Unit Tests (using pytest) for:

setting .display_name during OWUModel.__init__()
"""

from unittest.mock import patch, Mock


from dify_open_webui_adapter import (
    OWUModel,
    DifyAppType,
)

# Pytest unit tests  ###########################################################


class TestName:

    def test1(_, config_wf1, app_direct_wf1, app_given_name_wf1):
        config = config_wf1
        app = app_direct_wf1

        model = OWUModel(config, app)

        opt = model.display_name
        print(opt)

        assert isinstance(opt, str)
        assert opt == app_given_name_wf1

    # FIXME update
