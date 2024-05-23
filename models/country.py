from pydantic import BaseModel
from typing import Optional

class Country(BaseModel):
    name: str
    size: Optional[int]
   