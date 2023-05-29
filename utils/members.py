from dataclasses import dataclass, field
from datetime import datetime
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class Member():
    id: int = field(default=0, compare=False) # Discord ID
    nickname: str = field(default="", compare=True)
    role: int = field(default=0, compare=False)
    name: Optional[str] = field(default=None, compare=False)
    birthday: Optional[datetime] = field(default=None, compare=True)
    projects: list[int] = field(default_factory=list, compare=False)
    retro: Optional[int] = field(default=None, compare=False)