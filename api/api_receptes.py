from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from core.connection_manager import ConnectionManager
from schemas.recepta import ReceptaCreate, ReceptaResponse
from services.receptes_data_service import ReceptesDataService

receptes_data_service = ReceptesDataService()
receptes_connection_manager = ConnectionManager[ReceptaResponse]()

router = APIRouter()

# --- WEBSOCKET ENDPOINT FOR REAL-TIME UPDATES ---
@router.websocket("/ws/receptes")
async def websocket_endpoint(websocket: WebSocket):
    await receptes_connection_manager.connect(websocket)
    receptes = receptes_data_service.read_receptes()
    receptes_response = [ReceptaResponse.model_validate(r) for r in receptes]
    await receptes_connection_manager.send(websocket, receptes_response)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        receptes_connection_manager.disconnect(websocket)

# --- MÈTODES CRUD (Estil SQLAlchemy 2.0 Atòmic) ---

# 1. Crear una recepta
@router.post("/receptes", response_model=ReceptaResponse)
async def create_recepta(recepta: ReceptaCreate):
    recepta_creada = receptes_data_service.create_recepta(recepta)
    # await manager.broadcast_receptes(db)
    if not recepta_creada:
        raise HTTPException(status_code=404, detail="No s'ha pugut crear la recepta")
    return recepta_creada

# 2. Consultar totes les receptes
@router.get("/receptes", response_model=list[ReceptaResponse])
def read_receptes():
    receptes = receptes_data_service.read_receptes()
    return receptes

# 3. Consultar una sola recepta per ID
@router.get("/receptes/{id}", response_model=ReceptaResponse)
def read_recepta(id: int):
    recepta = receptes_data_service.read_recepta(id)    
    if not recepta:
        raise HTTPException(status_code=404, detail="Recepta no trobada")
    return recepta

# 4. Actualitzar una recepta
@router.put("/receptes/{id}", response_model=ReceptaResponse)
async def update_recepta(id: int, recepta: ReceptaCreate):
    recepta_actualitzada = receptes_data_service.update_recepta(id, recepta)
    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="No existeix la recepta per actualitzar")   
    # await manager.broadcast_receptes(db)
    return recepta_actualitzada

# 5. Esborrar una recepta (DELETE Atòmic)
@router.delete("/receptes/{id}", response_model=ReceptaResponse)
async def delete_recepta(id: int):
    recepta_db = receptes_data_service.delete_recepta(id)
    if not recepta_db:
        raise HTTPException(status_code=404, detail="No s'ha trobat la recepta per esborrar")
    recepta_esborrada = ReceptaResponse.model_validate(recepta_db)
    # await manager.broadcast_receptes(db)
    return recepta_esborrada

# 6. Bonus: Fer Like (Increment atòmic)
@router.post("/receptes/{id}/like", response_model=ReceptaResponse)
async def fer_like(id: int):
    recepta_actualitzada = receptes_data_service.incrementar_likes(id)
    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="Recepta no trobada")   
    # await manager.broadcast_receptes(db)
    return recepta_actualitzada