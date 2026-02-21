from fastapi import WebSocket
from typing import Generic, TypeVar
from pydantic import BaseModel

T= TypeVar("T", bound=BaseModel)

class ConnectionManager(Generic[T]):
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, websocket: WebSocket, data: list[T]):
        json_data = [r.model_dump(by_alias=True) for r in data]
        await websocket.send_json(json_data)
        
    async def broadcast(self, data: list[T]):
         json_data = [r.model_dump(by_alias=True) for r in data]
         for websocket in self.active_connections:
            try:
                await websocket.send_json(json_data)
            except:
                pass

