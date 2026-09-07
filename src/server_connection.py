import asyncio
import json
import uuid
import websockets

URI = "ws://localhost:8080/ws"

async def send_message(websocket, conversation_id: str, content: str):
    message = {
        "type": "message.send",
        "requestId": str(uuid.uuid4()),
        "payload": {
            "conversationId": conversation_id,
            "content": content,
        },
    }
    await websocket.send(json.dumps(message))
    #response = await websocket.recv()
    #print(response)
    #return response

async def maintain_connection(app):
    """Reconnect loop; stores the live socket on app.state."""
    while True:
        try:
            async with websockets.connect(URI, open_timeout=5) as ws:
                app.state.ws = ws
                # Keep the connection alive by waiting for close / reading frames
                async for _ in ws:
                    pass  # or dispatch inbound messages later
        except (OSError, asyncio.TimeoutError, websockets.InvalidHandshake) as e:
            print(f"WS down: {e}; retrying…")
        finally:
            app.state.ws = None
        await asyncio.sleep(2)

