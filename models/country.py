from pydantic import BaseModel
from typing import Optional

class Country(BaseModel):
    world_code: str
    name: Optional[str] = None
    size: Optional[int] = None
    population: Optional[int] = None
    density: Optional[int] = None


