from pydantic import BaseModel
from typing import Optional

class Continent(BaseModel):
    world_code: Optional[str] = None
    name: Optional[str] = None
    size: int
    countries: Optional[list] = []

