from fastapi import APIRouter, WebSocket


r = APIRouter(prefix="/chat", tags=["Chats"])


@r.websocket("/ws")
async def echo(
    websocket: WebSocket,
):
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        await websocket.send_text(text)
