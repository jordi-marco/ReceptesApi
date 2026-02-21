from fastapi import FastAPI
from api.api_receptes import router as receptes_router

# --- INSTÀNCIA DE L'API ---
app = FastAPI(title="API Receptes 1.0")

app.include_router(receptes_router)