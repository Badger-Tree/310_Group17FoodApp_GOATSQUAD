from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeliveryBase(BaseModel):
    order_id: str
    address_id: str

class DeliveryCreate(DeliveryBase):
    courier_id: Optional[str] = None

class DeliveryUpdate(BaseModel):
    courier_id: Optional[str] = None


class DeliveryResponse(DeliveryBase):
    delivery_id: str
    courier_id: Optional[str] = None
    created_date: datetime
