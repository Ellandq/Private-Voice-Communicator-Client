import json
from unittest.mock import AsyncMock

import pytest

from communicator_client.domains.messaging import send_message


@pytest.mark.asyncio
async def test_send_message_sends_json_envelope():
    websocket = AsyncMock()

    await send_message(websocket, "conv-123", "hello")

    websocket.send.assert_awaited_once()
    raw = websocket.send.await_args.args[0]
    envelope = json.loads(raw)

    assert envelope["type"] == "message.send"
    assert envelope["payload"] == {
        "conversationId": "conv-123",
        "content": "hello",
    }
    assert isinstance(envelope["requestId"], str)
    assert len(envelope["requestId"]) > 0
