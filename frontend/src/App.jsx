import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const load = async () => {
      const res = await fetch("http://localhost:5000/api/status");
      const json = await res.json();
      setData(json);
    };
    load();
    const id = setInterval(load, 1000);
    return () => clearInterval(id);
  }, []);

  if (!data) return <p>Cargando...</p>;

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

      <h2>Tráfico total:</h2>
      <p>{data.traffic_count}</p>
    </div>
  );
}

export default App;
