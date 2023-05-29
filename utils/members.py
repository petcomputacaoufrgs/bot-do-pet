from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True, order=True)
class Member():
    id: int = field(default=0, compare=False) # Discord ID
    nickname: str = field(default=None, compare=True)
    role: int = field(default=0, compare=False)
    name: str = field(default=None, compare=False)
    birthday: datetime = field(default=None, compare=True)
    projects: list[int] = field(default_factory=list, compare=False)
    retro: int = field(default=0, compare=False)