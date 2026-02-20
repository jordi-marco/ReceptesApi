from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from schemas.recepta import ReceptaCreate, ReceptaResponse
from services import data_service


# --- GESTOR DE WEBSOCKETS ---
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def broadcast_receptes(self, db: Session):
#         stmt = select(ReceptaDB)
#         receptes_db = db.execute(stmt).scalars().all()
#         receptes = [ReceptaResponse.model_validate(r).model_dump(by_alias=True) for r in receptes_db]
        
#         for connection in self.active_connections:
#             try:
#                 await connection.send_json(receptes)
#             except:
#                 pass

# manager = ConnectionManager()

# --- INSTÀNCIA DE L'API ---
app = FastAPI(title="API Receptes 1.0")

# --- WEBSOCKET ENDPOINT FOR REAL-TIME UPDATES ---
# @app.websocket("/ws/receptes")
# async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
#     await manager.connect(websocket)
#     stmt = select(ReceptaDB)
#     receptes_db = db.execute(stmt).scalars().all()
#     receptes = [ReceptaResponse.model_validate(r).model_dump(by_alias=True) for r in receptes_db]
#     await websocket.send_json(receptes)
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# --- MÈTODES CRUD (Estil SQLAlchemy 2.0 Atòmic) ---

data_service = data_service.DataService()

# 1. Crear una recepta
@app.post("/receptes", response_model=ReceptaResponse)
async def create_recepta(recepta: ReceptaCreate):
    recepta_creada = data_service.create_recepta(recepta)
    # await manager.broadcast_receptes(db)
    return recepta_creada

# 2. Consultar totes les receptes
@app.get("/receptes", response_model=list[ReceptaResponse])
def read_receptes():
    recepta_creada = data_service.read_receptes()
    if not recepta_creada:
        raise HTTPException(status_code=404, detail="No s'ha pugut crear la recepta")
    return recepta_creada

# 3. Consultar una sola recepta per ID
@app.get("/receptes/{id}", response_model=ReceptaResponse)
def read_recepta(id: int):
    recepta = data_service.read_recepta(id)    
    if not recepta:
        raise HTTPException(status_code=404, detail="Recepta no trobada")
    return recepta

# 4. Actualitzar una recepta
@app.put("/receptes/{id}", response_model=ReceptaResponse)
async def update_recepta(id: int, recepta: ReceptaCreate):
    recepta_actualitzada = data_service.update_recepta(id, recepta)
    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="No existeix la recepta per actualitzar")   
    # await manager.broadcast_receptes(db)
    return recepta_actualitzada

# 5. Esborrar una recepta (DELETE Atòmic)
@app.delete("/receptes/{id}", response_model=ReceptaResponse)
async def delete_recepta(id: int):
    recepta_db = data_service.delete_recepta(id)
    if not recepta_db:
        raise HTTPException(status_code=404, detail="No s'ha trobat la recepta per esborrar")
    recepta_esborrada = ReceptaResponse.model_validate(recepta_db)
    # await manager.broadcast_receptes(db)
    return recepta_esborrada

# 6. Bonus: Fer Like (Increment atòmic)
@app.post("/receptes/{id}/like", response_model=ReceptaResponse)
async def fer_like(id: int):
    recepta_actualitzada = data_service.incrementar_likes(id)
    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="Recepta no trobada")   
    # await manager.broadcast_receptes(db)
    return recepta_actualitzada