from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router
from .routers.food_item import router as food_router
from app.routers.order import router as order_router
from app.routers.user import router as user_router
from app.routers.address import router as address_router
from app.routers.inventory_router import router as inventory_router

app = FastAPI()



app.include_router(order_router)