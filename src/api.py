from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from server_connection import maintain_connection, send_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ws = None
    task = asyncio.create_task(maintain_connection(app))
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

class Message(BaseModel):
    conversation_id: str
    content: str


@app.post("/message")
async def post_message(message: Message):
    ws = app.state.ws
    if ws is None:
        raise HTTPException(status_code=503, detail="WebSocket connection not established")
    await send_message(ws, message.conversation_id, message.content)
    return {"ok": True}
