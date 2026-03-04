# HACK rm file

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
