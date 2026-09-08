import asyncio
import websockets


URI = "ws://localhost:8080/ws"

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