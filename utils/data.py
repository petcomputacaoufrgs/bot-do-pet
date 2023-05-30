from dataclasses import dataclass, field
from utils.dictjson import dictJSON
from utils.projects import Project
from utils.members import Member

@dataclass
class Data:
    Channels: dictJSON = field(default_factory=lambda: dictJSON("data/channels.json"))
    Interpet: dictJSON = field(default_factory=lambda: dictJSON("data/interpet.json"))
    Key: dictJSON = field(default_factory=lambda: dictJSON("data/key.json"))
    Leadership: dictJSON = field(default_factory=lambda: dictJSON("data/leadership.json"))
    Payments: dictJSON = field(default_factory=lambda: dictJSON("data/payment.json"))
    Members: dictJSON[Member] = field(default_factory=lambda: dictJSON("data/petianes.json", dumper=lambda o: o.to_json(), loader=lambda k, v: (int(k), Member.from_json(v))))
    Projects: dictJSON[Project] = field(default_factory=lambda: dictJSON("data/projects.json", dumper=lambda o: o.to_json(), loader=lambda k, v: (int(k), Project.from_json(v))))
    Roles: dictJSON = field(default_factory=lambda: dictJSON("data/roles.json"))
    Schedule: dictJSON = field(default_factory=lambda: dictJSON("data/schedule.json"))
    Secrets: dictJSON = field(default_factory=lambda: dictJSON("data/secrets.json"))    