import json
from dataclasses import dataclass, asdict


@dataclass
class Network:
    bytes_recieved: int
    bytes_sent: int


@dataclass
class Disk:
    read_count: int
    write_count: int


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
