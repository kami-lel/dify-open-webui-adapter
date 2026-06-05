---
name: dify-open-webui-adapter AGENTS
---

# dify-open-webui-adapter

## Overview

A single-file Python adapter (`dify_open_webui_adapter.py`) that exposes Dify
Apps (Workflow and Chatflow) as Open WebUI models via OWU's Pipe Function
mechanism. All production code lives in one file — no source package hierarchy.
Tests live under `tests/`.

## Architecture

### Entity relationship

```
Pipe  1──*  OWUModel  1──1  BaseDifyApp (WorkflowApp | ChatflowApp)
```

- `Pipe.__init__` iterates `APP_MODEL_CONFIGS`, creates one `OWUModel` + one
  `WorkflowApp`/`ChatflowApp` per entry, then cross-links them
  (`app.model = model`).
- `Pipe.pipes()` returns a list of `{"id": ..., "name": ...}` dicts for OWU.
- `Pipe.pipe()` dispatches each OWU request to the matching `OWUModel.reply()`.

### Key classes

| Class | Role |
|---|---|
| `AppModelConfig` | Pydantic model; validates one entry of `APP_MODEL_CONFIGS` |
| `PipeCall` | Pydantic model; wraps a single OWU `pipe()` invocation (body, user, metadata) |
| `BaseDifyApp` | Abstract base for Dify app logic; calls Dify Backend API |
| `WorkflowApp(BaseDifyApp)` | Implements Workflow-specific endpoint, payload, and blocking reply |
| `ChatflowApp(BaseDifyApp)` | Implements Chatflow-specific endpoint, payload, and blocking reply |
| `OWUModel` | OWU-side logic container; owns one `AppModelConfig` + one app; resolves streaming |
| `ResponseStream` | Iterator over a streaming SSE response from Dify |
| `_SSELine` / `_SSEType` | Internal SSE parsing helpers; not part of the public API |
| `Pipe` | Top-level OWU Pipe Function class; owns `models{}` and `apps{}` dicts keyed by `model_id` |

### Dify API endpoints used

| App type | Endpoint | Notes |
|---|---|---|
| Both | `GET /info` | Fetch app type (`mode`) and name at init time |
| Workflow | `POST /workflows/run` | Single-turn; reply extracted from `data.outputs.<identifier>` |
| Chatflow | `POST /chat-messages` | Multi-turn; reply extracted from `answer`; `conversation_id` from `metadata.chat_id` |

### Streaming (SSE) model

- `OWUModel.is_using_stream` → `True` when `call.body.stream` is `True` AND
  `config.disallows_streaming` is `False`.
- `BaseDifyApp.reply()` returns a `ResponseStream` iterator (streaming) or a
  plain `str` (blocking).
- `ResponseStream.__next__` consumes `iter_lines()`, parses each raw bytes
  line via `_SSELine.parse_from_raw_line()`, yields text chunks, and raises
  `StopIteration` on `IS_END` events (`workflow_finished` | `message_end`).
- SSE text-carrying events: `text_chunk` (WF, key `data.text`) and `message`
  (CF, key `answer`).

## Coding Conventions

- use `i`, `j`, `k` for loop counters; `_` for intentionally unused variables
- function names start with a verb: `create_app`, `open_chat_response`
- boolean names start with `is_` or `has_`: `is_using_stream`
- class names are PascalCase: `WorkflowApp`, `OWUModel`
- constants are `UPPER_CASE_WITH_UNDERSCORES`: `APP_MODEL_CONFIGS`
- inline comments: two spaces before `#`, one space after — `x = 1  # comment`
- lines must not exceed 80 characters

## Environment Setup

```bash
pip install -r requirements.txt
```

Dependencies: `pydantic`, `requests`, `pytest`, `pytest-asyncio`.

User-editable constants at the top of `dify_open_webui_adapter.py`:

| Constant | Type | Default | Purpose |
|---|---|---|---|
| `DIFY_BACKEND_API_BASE_URL` | `str` | `"https://api.dify.ai/v1"` | Dify API base URL |
| `APP_MODEL_CONFIGS` | `list[dict]` | `[]` | One dict per Dify app/OWU model connection |
| `DEBUG_PIPE_DIRECT_RESPONSE` | `bool` | `False` | Short-circuit `pipe()` to echo raw request |
| `DEBUG_CONVERSATION_ROUND_DIRECT_RESPONSE` | `bool` | `False` | Short-circuit stream to echo raw SSE |

`APP_MODEL_CONFIGS` dict keys: `key` (required), `model_id` (required),
`name` (optional), `disallows_streaming` (optional, default `False`),
`query_input_field_identifier` (WF only, default `"query"`),
`reply_output_variable_identifier` (WF only, default `"answer"`).

## Common Commands

```bash
# run all tests
pytest

# run tests for a specific domain
pytest tests/app/
pytest tests/pipe/
pytest tests/rs/
```

## Testing

### Layout

```
tests/
├── __init__.py          # shared helpers: create_pipe_call*, create_mock_resp_*,
│                        #   load_stream_entries_testee, convert_key2authorization
├── conftest.py          # global fixtures: pipe_obj, config_*, app_direct_*,
│                        #   mock_*, patch_target_*, model_id_*, auth_key_*
├── rs/                  # ResponseStream tests (init, iter, next, errors)
│   └── conftest.py      # testee_cf1 / testee_wf1 fixtures
├── pipe/                # Pipe class tests (init, pipes(), pipe(), errors)
├── app/
│   ├── base/            # BaseDifyApp tests (create_app, header, info)
│   ├── cf/              # ChatflowApp tests
│   └── wf/              # WorkflowApp tests
├── model/               # OWUModel tests
├── call/                # PipeCall tests (init, model_id, username, message)
├── config/              # AppModelConfig tests (validation, fields)
└── testee/              # JSON fixtures for SSE stream entries
    ├── stream_entries_cf*.json   # Chatflow SSE payloads (event: "message")
    └── stream_entries_wf*.json   # Workflow SSE payloads (event: "text_chunk")
```

Test file naming: `<domain>-<aspect>_test.py`, e.g. `app-cf-reply-block_test.py`.

### Fixture conventions

- `pipe_obj` — fully-initialized `Pipe` instance with 4 apps/models
  (wf1, wf2, cf1, cf2); `scope="class"`.
- `app_direct_*` — `WorkflowApp`/`ChatflowApp` created directly (bypass
  `create_app`); `scope="class"`.
- `patch_target_get/post/configs` — string paths for `unittest.mock.patch`.
- `mock_assertee_*` — `(args, kwargs)` tuples used to assert `mock.assert_called_once_with`.
- `mock_chat_block_*` / `mock_chat_stream_*` — `Mock` / `MagicMock` HTTP
  response objects.
- `create_pipe_call(model_id, stream, messages, ...)` — builds a `PipeCall`;
  default message is `[{"role": "user", "content": "Hello Dify"}]`;
  model prefixed as `"dify2owu.<model_id>"`.

## Notes for AI

- **single source file** — do not propose splitting `dify_open_webui_adapter.py`
  into multiple modules; the single-file constraint is intentional (OWU Pipe
  Functions must be a single file)
- **`app.model` back-reference** — `BaseDifyApp` instances carry a `.model`
  attribute set after construction by `Pipe.__init__`; it is `None` until then
- **`OWUModel.call`** — set per-round by `OWUModel.reply(call)`; `None` at
  init time; never persist state across rounds except `ChatflowApp._conversation_id`
- **scripts/** — contains only Git hook scripts and a submodule; not part of
  the adapter logic
- `config_raw_wf2` has no fixture — it is built inline inside `configs_mux`
