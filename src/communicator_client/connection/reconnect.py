import asyncio
import os

import websockets


# Inside Docker, localhost is this container — use host.docker.internal (Desktop)
# or a Compose service name to reach a server outside it.
URI = os.environ.get("SERVER_WS_URI", "ws://localhost:5164/ws")

async def maintain_connection(app):
    """Reconnect loop; stores the live socket on app.state."""
    while True:
        try:
            # Connect to the server and store the socket in app.state
            async with websockets.connect(URI, open_timeout=5) as ws:
                app.state.ws = ws
                async for _ in ws:
                    pass
        except (OSError, asyncio.TimeoutError, websockets.InvalidHandshake) as e:
            print(f"WS down: {e}; retrying…")
        finally:
            app.state.ws = None
        await asyncio.sleep(2)