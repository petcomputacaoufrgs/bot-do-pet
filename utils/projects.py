from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class Project():
    id: int = field(default=0, compare=False)
    name: str = field(default="", compare=True)
    description: Optional[str] = field(default=None, compare=False)
    leader: Optional[int] = field(default=None, compare=False)
    members: list[int] = field(default_factory=list, compare=False)
    channels: list[int] = field(default_factory=list, compare=False)
    color: int = field(default=0xFFFFFF, compare=False)
    time: int = field(default=0, compare=False)