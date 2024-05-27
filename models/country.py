from typing import Optional
from pydantic import BaseModel


class Country(BaseModel):
    world_code: str
    name: Optional[str] = None
    size: Optional[int] = None
    population: Optional[int] = None
    density: Optional[int] = None
    climate_zone: Optional[str] = None
