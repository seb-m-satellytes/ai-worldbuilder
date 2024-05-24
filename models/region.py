from typing import Optional
from pydantic import BaseModel

class Region(BaseModel):
    world_code: str
    name: Optional[str] = None
    population: Optional[int] = None
