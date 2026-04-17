"""
Integrating between: Open WebUI (abbr OWU) and Dify,
by exposing a Dify **app** (supporting Workflow and Chatflow)
as Open WebUI **model**.

Connecting with Dify app via *Dify Backend API*
and with OWU via *Pipe Function*.

Q.v. ``https://github.com/kami-lel/dify-open-webui-adapter``
"""

# adapter version
__version__ = "2.2.1-alpha"
__author__ = "kamiLeL"


# config  ######################################################################
DIFY_BACKEND_API_BASE_URL = "https://api.dify.ai/v1"
APP_MODEL_CONFIGS = []


# debug flags  =================================================================
DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE = False
DEBUG_PIPE_DIRECT_RESPONSE = False


# end of config  ###############################################################

# pylint: disable=wrong-import-position

from pydantic import BaseModel

# Dify side  ###################################################################
# Dify constants  ==============================================================


class BaseDifyApp:  # ==========================================================

    pass


class WorkflowApp(BaseDifyApp):  # =============================================

    pass


class ChatflowApp(BaseDifyApp):  # =============================================

    pass


# OWU side  ####################################################################
# OWU constants  ===============================================================


class OWUModel:  # =============================================================

    pass


class Pipe:  # =================================================================
    """
    Pipe class required by OWU Pipe Function
    """

    class Valves(BaseModel):  # pylint: disable=missing-class-docstring
        pass  # configuration via Python constants

    def __init__(self):
        pass

    def pipes(self):
        pass

    async def pipe(self, body, __user__, __metadata__):
        pass
