from typing import Optional
from models.settlement import Settlement


class Metropolis(Settlement):
    year_first_mentioned: Optional[int] = None
