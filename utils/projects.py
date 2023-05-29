from dataclasses import dataclass, field

@dataclass(slots=True, order=True)
class Project():
    id: int = field(default=0, compare=False)
    name: str = field(default="", compare=True)
    description: str = field(default="", compare=False)
    leader: int = field(default=0, compare=False)
    members: list[int] = field(default_factory=list, compare=False)
    channels: list[int] = field(default_factory=list, compare=False)
    color: int = field(default=0xFFFFFF, compare=False)