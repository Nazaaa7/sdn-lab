from flask import Flask, jsonify
import threading
import random
import time

from network import Host, Router, TrafficType
from sdn_controller import SimpleSDNController
from analyzer import TrafficAnalyzer

app = Flask(__name__)

controller = SimpleSDNController()
analyzer = TrafficAnalyzer(controller)

class NetworkSimulator:
    def __init__(self):
        self.controller = controller
        self.running = False
        self.setup_network()

    def setup_network(self):
        for i in range(1, 7):
            h = Host(f"H{i}", f"10.0.0.{i}")
            if i == 4:
                h.role = "web_server"
            if i == 5:
                h.role = "printer"
            self.controller.add_host(h)

        r = Router("R1")
        self.controller.add_router(r)

    def generate_normal_traffic(self):
        while self.running:
            for host in self.controller.hosts.values():
                dst = f"H{random.randint(1, 6)}"
                pkt = host.send_packet(dst)
                self.controller.route_packet(pkt)

            time.sleep(0.1)

    def generate_attack_traffic(self):
        while self.running:
            if random.random() < 0.1:
                attacker = self.controller.hosts[f"H{random.randint(1,6)}"]
                for _ in range(40):
                    pkt = attacker.send_packet("H4", traffic_type=TrafficType.ATTACK)
                    controller.route_packet(pkt)

            time.sleep(0.5)

    def start(self):
        self.running = True
        threading.Thread(target=self.generate_normal_traffic, daemon=True).start()
        threading.Thread(target=self.generate_attack_traffic, daemon=True).start()

sim = NetworkSimulator()
sim.start()

@app.route("/api/status")
def status():
    return jsonify({
        "hosts": [
            {
                "id": h.id,
                "ip": h.ip,
                "role": h.role
            }
            for h in controller.hosts.values()
        ],
        "blocked": list(controller.blocked_hosts),
        "traffic_count": len(controller.traffic_history)
    })

if __name__ == "__main__":
    app.run(port=5000)
