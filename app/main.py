from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router
from .routers.food_item import router as food_router
from app.routers.user import router as user_router
from app.routers.address import router as address_router
from app.routers.authentication import router as authentication
from app.routers.carts import router as carts_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

app.include_router(carts_router)
app.include_router(cartItems_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(food_router)
app.include_router(authentication)
