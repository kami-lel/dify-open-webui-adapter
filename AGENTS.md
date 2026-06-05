---
name: dify-open-webui-adapter AGENTS.md
alwaysApply: true
---

# dify-open-webui-adapter AGENTS.md

## Project Overview

Single-file Python adapter (`dify_open_webui_adapter.py`) — exposes Dify Apps
(Workflow and Chatflow) as Open WebUI models via OWU's Pipe Function mechanism.
All production code lives in one file; tests live under `tests/`.

### Entity Relationships

```
Pipe  1──*  OWUModel  1──1  BaseDifyApp (WorkflowApp | ChatflowApp)
```

- `Pipe.__init__` — iterates `APP_MODEL_CONFIGS`, creates 1 `OWUModel` +
  1 `WorkflowApp`/`ChatflowApp` per entry, then cross-links (`app.model = model`)
- `Pipe.pipes()` — returns `[{"id": ..., "name": ...}]` list for OWU
- `Pipe.pipe()` — dispatches each OWU request to the matching `OWUModel.reply()`

### Key Classes

| Class | Role |
|---|---|
| `AppModelConfig` | Pydantic model; validates 1 entry of `APP_MODEL_CONFIGS` |
| `PipeCall` | Pydantic model; wraps a single OWU `pipe()` call (body, user, metadata) |
| `BaseDifyApp` | abstract base for Dify app logic; calls Dify Backend API |
| `WorkflowApp(BaseDifyApp)` | Workflow-specific endpoint, payload, and blocking reply |
| `ChatflowApp(BaseDifyApp)` | Chatflow-specific endpoint, payload, and blocking reply |
| `OWUModel` | OWU-side container; owns 1 `AppModelConfig` + 1 app; resolves streaming |
| `ResponseStream` | iterator over a streaming SSE response from Dify |
| `_SSELine` / `_SSEType` | internal SSE parsing helpers; not public API |
| `Pipe` | top-level OWU Pipe Function class; owns `models{}` and `apps{}` keyed by `model_id` |

### Dify API Endpoints

| App Type | Endpoint | Notes |
|---|---|---|
| Both | `GET /info` | fetch app type (`mode`) and name at init |
| Workflow | `POST /workflows/run` | single-turn; reply from `data.outputs.<identifier>` |
| Chatflow | `POST /chat-messages` | multi-turn; reply from `answer`; `conversation_id` from `metadata.chat_id` |

### Streaming (SSE) Model

- `OWUModel.is_using_stream` — `True` when `call.body.stream` is `True` AND
  `config.disallows_streaming` is `False`
- `BaseDifyApp.reply()` — returns `ResponseStream` iterator (streaming) or
  plain `str` (blocking)
- `ResponseStream.__next__` — consumes `iter_lines()`, parses raw bytes via
  `_SSELine.parse_from_raw_line()`, yields text chunks, raises `StopIteration`
  on `IS_END` events (`workflow_finished` | `message_end`)
- SSE text events: `text_chunk` (WF, key `data.text`); `message` (CF, key `answer`)

### Agent Constraints

- **single source file** — never split `dify_open_webui_adapter.py`; the
  single-file constraint is intentional (OWU Pipe Functions must be 1 file)
- **`app.model` back-reference** — `BaseDifyApp` instances carry a `.model`
  attribute set after construction by `Pipe.__init__`; `None` until then
- **`OWUModel.call`** — set per-round by `OWUModel.reply(call)`; `None` at
  init; never persist state across rounds except `ChatflowApp._conversation_id`
- **`scripts/`** — Git hook scripts and submodule only; not part of adapter logic
- **`config_raw_wf2`** — no fixture; built inline inside `configs_mux`

## Dev Environment Tips

- Python 3 required; install deps with `pip install -r requirements.txt`
- dependencies: `pydantic`, `requests`, `pytest`, `pytest-asyncio`
- user-editable constants live at the top of `dify_open_webui_adapter.py`:

| Constant | Type | Default | Purpose |
|---|---|---|---|
| `DIFY_BACKEND_API_BASE_URL` | `str` | `"https://api.dify.ai/v1"` | Dify API base URL |
| `APP_MODEL_CONFIGS` | `list[dict]` | `[]` | one dict per Dify app / OWU model connection |
| `DEBUG_PIPE_DIRECT_RESPONSE` | `bool` | `False` | short-circuit `pipe()` to echo raw request |
| `DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE` | `bool` | `False` | short-circuit stream to echo raw SSE |

`APP_MODEL_CONFIGS` entry keys:

- `key` *(required)* — Dify Backend Service API secret key
- `model_id` *(required)* — OWU model ID
- `name` *(optional)* — OWU model display name; fetched from Dify if absent
- `disallows_streaming` *(optional, default `False`)* — force blocking mode
- `query_input_field_identifier` *(WF only, default `"query"`)* — Start node input field
- `reply_output_variable_identifier` *(WF only, default `"answer"`)* — End node output variable

## Build and Test Commands

```bash
# install dependencies
pip install -r requirements.txt

# run full test suite
pytest

# run tests by domain
pytest tests/app/
pytest tests/pipe/
pytest tests/rs/
pytest tests/model/
pytest tests/call/
pytest tests/config/
```

## Code Style

- Python; adhere to PEP 8
- max line length: 80 characters
- docstrings: Sphinx/reStructuredText style
- loop counters: `i`, `j`, `k`; unused variables: `_`
- function names start with a verb: `create_app`, `open_chat_response`
- boolean names start with `is_` or `has_`: `is_using_stream`
- class names: PascalCase — `WorkflowApp`, `OWUModel`
- constants: `UPPER_CASE_WITH_UNDERSCORES` — `APP_MODEL_CONFIGS`
- inline comments: 2 spaces before `#`, 1 space after — `x = 1  # comment`

## Testing Instructions

### Layout

```
tests/
├── __init__.py      # shared helpers: create_pipe_call*, create_mock_resp_*,
│                    #   load_stream_entries_testee, convert_key2authorization
├── conftest.py      # global fixtures: pipe_obj, config_*, app_direct_*,
│                    #   mock_*, patch_target_*, model_id_*, auth_key_*
├── rs/              # ResponseStream tests (init, iter, next, errors)
│   └── conftest.py  # testee_cf1 / testee_wf1 fixtures
├── pipe/            # Pipe class tests (init, pipes(), pipe(), errors)
├── app/
│   ├── base/        # BaseDifyApp tests (create_app, header, info)
│   ├── cf/          # ChatflowApp tests
│   └── wf/          # WorkflowApp tests
├── model/           # OWUModel tests
├── call/            # PipeCall tests (init, model_id, username, message)
├── config/          # AppModelConfig tests (validation, fields)
└── testee/          # JSON fixtures for SSE stream entries
    ├── stream_entries_cf*.json  # Chatflow SSE payloads (event: "message")
    └── stream_entries_wf*.json  # Workflow SSE payloads (event: "text_chunk")
```

### File Naming

`<domain>-<aspect>_test.py` — e.g., `app-cf-reply-block_test.py`

### Fixture Conventions

- `pipe_obj` — fully initialized `Pipe` with 4 apps/models (wf1, wf2, cf1, cf2);
  `scope="class"`
- `app_direct_*` — `WorkflowApp`/`ChatflowApp` created directly (bypass
  `create_app`); `scope="class"`
- `patch_target_get/post/configs` — string paths for `unittest.mock.patch`
- `mock_assertee_*` — `(args, kwargs)` tuples for `mock.assert_called_once_with`
- `mock_chat_block_*` / `mock_chat_stream_*` — `Mock`/`MagicMock` HTTP response objects
- `create_pipe_call(model_id, stream, messages, ...)` — builds a `PipeCall`;
  default message `[{"role": "user", "content": "Hello Dify"}]`;
  model prefixed as `"dify2owu.<model_id>"`

## PR Instructions

- run `pytest` and ensure all tests pass before committing
- commit messages: `<type>: <short summary>` (e.g., `fix: correct SSE end event`)
- do not commit changes to `DIFY_BACKEND_API_BASE_URL`, `APP_MODEL_CONFIGS`, or
  debug flags — those are user configuration, not source
- `scripts/` is a Git submodule (`hooks_utility`); do not modify its contents

## Security Considerations

- `APP_MODEL_CONFIGS` contains Dify API secret keys — never log, print, or
  expose key values in output, error messages, or test fixtures
- debug flags (`DEBUG_PIPE_DIRECT_RESPONSE`,
  `DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE`) echo raw request/response data;
  must remain `False` in production
