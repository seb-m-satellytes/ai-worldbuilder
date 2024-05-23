from pydantic import BaseModel
from typing import Optional

class City(BaseModel):
    name: str
    population: int
    year_first_mentioned: Optional[int] = None
