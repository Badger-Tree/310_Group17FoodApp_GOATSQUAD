from pydantic import BaseModel
from typing import List

class Role(BaseModel):
    role_id: int
    role_name: str
    permissions: List[Permission]