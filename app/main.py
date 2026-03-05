from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router
from .routers.food_item import router as food_router

from app.routers.user import router as user_router
from app.routers.address import router as address_router
from app.routers.restaurants import router as restaurant_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

app.include_router(cartItems_router)

app.include_router(user_router)
app.include_router(address_router)
app.include_router(restaurant_router)
app.include_router(food_router)
