from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router
from app.routers.cart import router as cart_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

app.include_router(cartItems_router)
app.include_router(cart_router)


