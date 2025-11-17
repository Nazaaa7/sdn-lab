import matplotlib.pyplot as plt
import numpy as np

class TrafficAnalyzer:
    def __init__(self, controller):
        self.controller = controller

    def show_traffic(self):
        data = list(self.controller.traffic_history)
        if not data:
            print("No hay datos todavía.")
            return

        timestamps = [d[0] for d in data]
        attack_flags = [1 if d[3] == "attack" else 0 for d in data]

        plt.plot(timestamps, np.cumsum(attack_flags))
        plt.title("Ataques detectados en el tiempo")
        plt.show()
