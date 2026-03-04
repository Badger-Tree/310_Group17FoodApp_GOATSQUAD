from fastapi import FastAPI
from app.routers.cartItems import router as cartItems_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

app.include_router(cartItems_router)


