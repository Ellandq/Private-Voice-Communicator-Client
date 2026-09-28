# Private Voice Communicator Client

Python protocol client and local HTTP bridge for Communicator. Early stage: text messaging over WebSocket (no voice yet).

## What it does today

The client keeps a persistent WebSocket to **Communicator.Server** and exposes a small local FastAPI app so other tools can send messages over HTTP.

| Piece | Role |
| --- | --- |
| `connection/reconnect.py` | Connects to the server WebSocket, reconnects on failure, stores the live socket on `app.state` |
| `domains/messaging.py` | Builds and sends `message.send` protocol payloads |
| `local_api/app.py` | FastAPI lifespan + `POST /message` bridge |

**Local API**

- `POST /message` with JSON `{ "conversation_id", "content" }`
- Returns `503` if the WebSocket is not connected yet

**Server protocol (outbound)**

```json
{
  "type": "message.send",
  "requestId": "<uuid>",
  "payload": {
    "conversationId": "...",
    "content": "..."
  }
}
```

Inbound server messages are not handled yet (the reconnect loop only keeps the socket open).

## Layout

```
Client/
  src/communicator_client/
    connection/     # WebSocket reconnect
    domains/        # Protocol helpers (messaging)
    local_api/      # FastAPI app
  tests/            # pytest (connection, domains, local_api)
  Dockerfile
  compose.yaml
  pyproject.toml
```

Package: `communicator-client` `0.1.0` · Python `>=3.11` · deps: FastAPI, Uvicorn, websockets, Pydantic.

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `SERVER_WS_URI` | `ws://localhost:5164/ws` | Communicator.Server WebSocket URL |

Inside Docker, `localhost` is the container itself. Compose sets:

`SERVER_WS_URI=ws://host.docker.internal:5164/ws`

so the client can reach a server running on the host (`dotnet run` → port **5164**). For a server in the same Compose network, use the service hostname instead (e.g. `ws://communicator.server:8080/ws`).

## Run locally

```powershell
cd Client
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn communicator_client.local_api.app:app --host 0.0.0.0 --port 8080
```

With Communicator.Server running on the host, leave `SERVER_WS_URI` unset (defaults to `ws://localhost:5164/ws`).

```powershell
pytest
```

## Run with Docker

Requires Communicator.Server reachable at the URI in `compose.yaml` (host port **5164** by default).

```powershell
cd Client
docker compose up --build
```

The image installs the package from `pyproject.toml` + `src/` and starts Uvicorn on port **8080** inside the container. Adjust `compose.yaml` port mappings so the host port targets that container port.

## Current limits

- Text send path only; no receive/dispatch of server events
- No voice, auth, or multi-conversation UI
- Docker networking must be configured explicitly (`host.docker.internal` or a shared network)
