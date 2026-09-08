import json
import uuid


async def send_message(websocket, conversation_id: str, content: str):
    """Send a message to the server."""
    message = {
        "type": "message.send",
        "requestId": str(uuid.uuid4()),
        "payload": {
            "conversationId": conversation_id,
            "content": content,
        },
    }
    await websocket.send(json.dumps(message))