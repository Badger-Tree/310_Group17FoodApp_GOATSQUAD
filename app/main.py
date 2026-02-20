from fastapi import FastAPI
from app.routers.customer import router as customers_router
from app.routers.address import router as address_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(customers_router)
app.include_router(address_router)