from pydantic import BaseModel
from typing import Optional

class Region(BaseModel):
    name: str
