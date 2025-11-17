from dataclasses import dataclass
from enum import Enum
import time
import random

class TrafficType(Enum):
    WEB = "web"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    ATTACK = "attack"
    PRINT = "print"

@dataclass
class Packet:
    src: str
    dst: str
    traffic_type: TrafficType
    size: int
    timestamp: float
    protocol: str

class Host:
    def __init__(self, host_id, ip, role="normal"):
        self.id = host_id
        self.ip = ip
        self.role = role
        self.traffic_count = 0
        self.last_reset = time.time()

    def send_packet(self, dst, traffic_type=TrafficType.WEB, protocol="TCP"):
        packet = Packet(
            src=self.id,
            dst=dst,
            traffic_type=traffic_type,
            size=random.randint(50, 1500),
            timestamp=time.time(),
            protocol=protocol
        )
        self.traffic_count += 1
        return packet

class Router:
    def __init__(self, router_id):
        self.id = router_id
        self.connections = []
        self.congestion = 0.0

    def connect(self, node_id):
        if node_id not in self.connections:
            self.connections.append(node_id)

    def process_packet(self, packet):
        self.congestion += packet.size / 10000.0
        self.congestion = max(0.0, self.congestion - 0.001)
        return True
