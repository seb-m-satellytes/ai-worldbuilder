from pydantic import BaseModel
from typing import Optional

class World(BaseModel):
    world_code: Optional[str] = None
    name: str
