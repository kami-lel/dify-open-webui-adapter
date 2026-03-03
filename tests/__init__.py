EXAMPLE_BASE_URL = "https://api.dify.ai/v1"

EXAMPLE_WORKFLOW_CONFIG = {
    "key": "eaJxetwz",
    "model_id": "example-workflow-model",
}

EXAMPLE_CHATFLOW_CONFIG = {
    "key": "u0caCsmD",
    "model_id": "example-chatflow-model",
    "name": "Example Chatflow Model/App",
}

EXAMPLE_CHATFLOW2_CONFIG = {
    "key": "YIFpPns6",
    "model_id": "example-chatflow-model-2",
    "name": "Aux Example Chatflow Model/App",
}


EXAMPLE_CONFIGS = [
    EXAMPLE_WORKFLOW_CONFIG,
    EXAMPLE_CHATFLOW_CONFIG,
    EXAMPLE_CHATFLOW2_CONFIG,
]


EXAMPLE_BODY1 = {
    "stream": True,
    "model": "dify_open_webui_adapter.example-chatflow-model",
    "messages": [{"role": "user", "content": "FIRST USER MESSAGE"}],
}


EXAMPLE_BODY2 = {
    "stream": True,
    "model": "dify_open_webui_adapter.example-chatflow-model",
    "messages": [
        {"role": "user", "content": "FIRST USER MESSAGE"},
        {"role": "assistant", "content": "FIRST BOT REPLY"},
        {"role": "user", "content": "SECOND USER MESSAGE"},
        {"role": "assistant", "content": "SECOND BOT REPLY"},
        {"role": "user", "content": "THIRD USER MESSAGE"},
    ],
}
