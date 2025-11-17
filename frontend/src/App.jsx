import { useEffect, useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend
);

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/status");
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("Error:", err);
      }
    };

    load();
    const id = setInterval(load, 1000);
    return () => clearInterval(id);
  }, []);

  if (!data) return <p>Cargando...</p>;

  // ---------------------------
  // 📊 Datos para el gráfico de barras
  // ---------------------------
  const barData = {
    labels: ["Tráfico total"],
    datasets: [
      {
        label: "Paquetes procesados",
        data: [data.traffic_count],
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }
    ]
  };

  // ---------------------------
  // 🟢🔴 Datos para gráfico de torta
  // ---------------------------
  const totalHosts = data.hosts.length;
  const blockedCount = data.blocked.length;
  const allowedCount = totalHosts - blockedCount;

  const pieData = {
    labels: ["Permitidos", "Bloqueados"],
    datasets: [
      {
        data: [allowedCount, blockedCount],
        backgroundColor: ["rgba(75, 192, 75, 0.6)", "rgba(255, 99, 132, 0.6)"]
      }
    ]
  };

  return (
    <div style={{ fontFamily: "Arial", padding: 20 }}>
      <h1>SDN – Estado de la red</h1>

      <h2>Hosts</h2>
      <ul>
        {data.hosts.map((h) => (
          <li key={h.id}>
            {h.id} — {h.ip} — {h.role}
          </li>
        ))}
      </ul>

      <h2>Bloqueados</h2>
      <ul>
        {data.blocked.length === 0 ? (
          <li>Ninguno</li>
        ) : (
          data.blocked.map((b) => <li key={b}>{b}</li>)
        )}
      </ul>

      <h2>Gráfico: tráfico total</h2>
      <div style={{ width: "400px", marginBottom: "30px" }}>
        <Bar data={barData} />
      </div>

      <h2>Gráfico: estado de hosts</h2>
      <div style={{ width: "350px" }}>
        <Pie data={pieData} />
      </div>
    </div>
  );
}

export default App;
