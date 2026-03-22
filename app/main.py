from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router
from .routers.food_item import router as food_router
from app.routers.authentication import router as authentication_router
from app.routers.user import router as user_router
from app.routers.address import router as address_router
from app.routers.inventory_router import router as inventory_router
from app.routers.order import router as order_router

app = FastAPI()

@app.get("/health")
def health():
    """checks if server is alive and returns ok status"""
    return {"status": "ok"}

@app.get("/")
def root():
    """creates a get endpoint at root url, confirms that api is running"""
    return {"message": "GoatSquad is Live!"}

app.include_router(authentication_router)
app.include_router(cartItems_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(food_router)
app.include_router(inventory_router)
app.include_router(order_router)