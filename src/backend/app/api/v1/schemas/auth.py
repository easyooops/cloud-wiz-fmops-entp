from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    token: str
