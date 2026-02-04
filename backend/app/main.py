from fastapi import FastAPI
from app.api.concepts import router as concepts_router

app = FastAPI(title="Validator Platform API")

app.include_router(concepts_router)
