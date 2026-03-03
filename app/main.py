from fastapi import FastAPI
from .routers.food_item import router as food_router

app = FastAPI()

#connects food router
app.include_router(food_router)
