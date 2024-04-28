import json
from dataclasses import dataclass, asdict


@dataclass
class Network:
    kilobytes_recieved: int
    kilobytes_sent: int

    def to_dict(self):
        return {"kilobytes_recieved": self.kilobytes_recieved, "kilobytes_sent": self.kilobytes_sent}


@dataclass
class Disk:
    kilobytes_read: int
    kilobytes_sent: int

    def to_dict(self):
        return {"kilobytes_read": self.kilobytes_read, "kilobytes_sent": self.kilobytes_sent}


@dataclass
class CPU:
    usage: float


@dataclass
class RAM:
    total: int
    used: int


@dataclass
class Data:
    cpu: CPU
    ram: RAM
    disk: Disk
    network: Network


@dataclass
class PC:
    pc_name: str
    pc_id: str
    timestamp: str
    data: Data

    def to_json(self):
        return json.dumps(asdict(self))
