# dify-open-webui-adapter README

Integrate **Open WebUI** and **Dify** by exposing a Dify App
(Workflow or Chatflow) as Open WebUI model using Open WebUI's
[Pipe Functions](https://docs.openwebui.com/features/plugin/functions/pipe/)













## configurations

User must configure these 2 constant in Python script before use:





### `DIFY_BACKEND_API_BASE_URL`

base URL to access Dify Backend Service API

<!-- TODO -->





### `APP_MODEL_CONFIGS`

a ``list`` of model/app config (each as ``dict``)

example for a single model/app::

    {
        "key": "...",             # Backend Service API secret key of Dify App
        "model_id": "model_id1",  # model id as used in Open WebUI
        "name": "First Model",    # model Name as appeared in Open WebUI
    }

example for ``APP_MODEL_CONFIGS``::

    APP_MODEL_CONFIGS = [
        {
            "key": "...",
            "model_id": "model_id1",
        },
        {
            ~  # config for 2nd app/model
        },
    ]

<!-- TODO: allow additional_inputs -->