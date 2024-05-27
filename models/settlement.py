from pydantic import BaseModel


class Settlement(BaseModel):
    name: str
    population: int
