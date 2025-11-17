import time
from collections import deque
from network import TrafficType

class SimpleSDNController:
    def __init__(self):
        self.hosts = {}
        self.routers = {}
        self.blocked_hosts = set()
        self.traffic_history = deque(maxlen=5000)
        self.attack_threshold = 50
        self.window_seconds = 1.0

    def add_host(self, host):
        self.hosts[host.id] = host

    def add_router(self, router):
        self.routers[router.id] = router

    def _count_from_host(self, host_id):
        now = time.time()
        return sum(1 for t, s, _, _, in self.traffic_history
                   if s == host_id and t >= now - self.window_seconds)

    def detect_attacks(self):
        for host_id in self.hosts:
            if host_id in self.blocked_hosts:
                continue
            if self._count_from_host(host_id) > self.attack_threshold:
                self.blocked_hosts.add(host_id)

    def route_packet(self, packet):
        self.traffic_history.append((
            packet.timestamp,
            packet.src,
            packet.dst,
            packet.traffic_type.value
        ))

        if packet.src in self.blocked_hosts:
            return {"action": "drop", "reason": "blocked"}

        self.detect_attacks()

        return {"action": "forward", "via": "R1"}
