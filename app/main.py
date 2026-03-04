from fastapi import FastAPI
from .routers.food_item import router as food_router

from app.routers.user import router as user_router
from app.routers.address import router as address_router

app = FastAPI()

#connects food router


app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user_router)
app.include_router(address_router)
app.include_router(food_router)