from typing import Optional
from pydantic import BaseModel


class Settlement(BaseModel):
    world_code: str
    name: Optional[str] = None
    population: int
