from pydantic import BaseModel
from typing import Optional

class Continent(BaseModel):
    world_code: str
    name: str
