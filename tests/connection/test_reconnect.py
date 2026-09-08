import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from communicator_client.connection.reconnect import maintain_connection


class MockApp:
    def __init__(self):
        self.state = SimpleNamespace(ws=None)


@pytest.mark.asyncio
async def test_sets_ws_while_connected():
    app = MockApp()
    ws = MagicMock()
    ready = asyncio.Event()
    closed = asyncio.Event()

    async def messages():
        ready.set()
        await closed.wait()
        if False:
            yield

    ws.__aiter__ = lambda self: messages()

    connect_cm = MagicMock()
    connect_cm.__aenter__ = AsyncMock(return_value=ws)
    connect_cm.__aexit__ = AsyncMock(return_value=None)

    with (
        patch(
            "communicator_client.connection.reconnect.websockets.connect",
            return_value=connect_cm,
        ),
        patch(
            "communicator_client.connection.reconnect.asyncio.sleep",
            new_callable=AsyncMock,
        ),
    ):
        task = asyncio.create_task(maintain_connection(app))
        await ready.wait()
        assert app.state.ws is ws

        closed.set()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
