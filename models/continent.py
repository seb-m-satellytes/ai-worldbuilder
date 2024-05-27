from typing import Optional
from pydantic import BaseModel


class Continent(BaseModel):
    world_code: Optional[str] = None
    name: Optional[str] = None
    size: int
    category: Optional[str] = None
    countries: Optional[list] = []
    coordinated_at: Optional[list] = []
    north_bound: Optional[int] = None
    south_bound: Optional[int] = None
    is_island: Optional[bool] = None
