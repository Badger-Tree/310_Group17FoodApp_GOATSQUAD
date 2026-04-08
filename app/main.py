from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.cart_router import router as cart_router
from .routers.food_item import router as food_router
from app.routers.authentication import router as authentication_router
from app.routers.user import router as user_router
from app.routers.address import router as address_router
from app.routers.inventory_router import router as inventory_router
from app.routers.restaurants import router as restaurant_router
from app.routers.inventory_router import router as inventory_router
from app.routers.order import router as order_router
from app.routers.delivery_router import router as delivery_router
from app.routers.staff_assignment_router import router as staff_assignment_router
from app.routers.track_items_router import router as track_items_router
from app.routers.review import router as review_router
from app.routers.favorite_router import router as favorite_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:5173",  # your Vite frontend
     "http://localhost:5174",
    "http://localhost:3000",  # optional, if you run CRA
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],     # allow GET, POST, etc.
    allow_headers=["*"],     # allow headers
)
# -------------------------
# Health & root endpoints
# -------------------------
@app.get("/health")
def health():
    """checks if server is alive and returns ok status"""
    return {"status": "ok"}

@app.get("/")
def root():
    """creates a get endpoint at root url, confirms that api is running"""
    return {"message": "GoatSquad is Live!"}

app.include_router(authentication_router)
app.include_router(cart_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(restaurant_router)
app.include_router(food_router)
app.include_router(inventory_router)
app.include_router(order_router)
app.include_router(delivery_router)
app.include_router(staff_assignment_router)
app.include_router(track_items_router)
app.include_router(review_router)
app.include_router(favorite_router)
