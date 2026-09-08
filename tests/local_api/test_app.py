from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from communicator_client.local_api import app as app_module


def test_post_message_returns_503_when_ws_missing():
    with patch.object(app_module, "maintain_connection", new_callable=AsyncMock):
        with TestClient(app_module.app) as client:
            client.app.state.ws = None
            response = client.post(
                "/message",
                json={"conversation_id": "conv-1", "content": "hello"},
            )

    assert response.status_code == 503
    assert response.json()["detail"] == "WebSocket connection not established"
