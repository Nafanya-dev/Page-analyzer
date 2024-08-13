from dataclasses import dataclass
from typing import Optional


@dataclass
class Url:
    name: str
    created_at: Optional[str] = None
    id: Optional[int] = None
