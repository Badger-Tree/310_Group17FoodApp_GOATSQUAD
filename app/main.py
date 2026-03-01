from fastapi import FastAPI
from app.routers.order import router as order_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(order_router)