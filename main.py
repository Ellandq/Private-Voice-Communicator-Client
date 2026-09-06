import asyncio
import json
import uuid

import websockets


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


async def main():
    uri = "ws://localhost:8080/ws"
    conversation_id = "22222222-2222-2222-2222-222222222222"

    
    async with websockets.connect(uri) as websocket:
        await send_message(websocket, conversation_id, "Hello!")
        await send_message(websocket, conversation_id, "Second message")
        await send_message(websocket, conversation_id, "Third message")


if __name__ == "__main__":
    asyncio.run(main())
