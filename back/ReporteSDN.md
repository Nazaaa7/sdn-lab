# SDN Lab

Breve guía para ejecutar y entender este proyecto de ejemplo de controlador SDN.

## Contenido clave
- Controlador SDN: [`sdn_controller.SimpleSDNController`](sdn_controller.py) — [sdn_controller.py](sdn_controller.py)  
- Modelos de red: [`network.Host`](network.py), [`network.TrafficType`](network.py) — [network.py](network.py)  
- Simulador y API (Flask): [main.py](main.py) — usa el controlador y expone `/api/status`  
- Analizador de tráfico: [`analyzer.TrafficAnalyzer`](analyzer.py) — [analyzer.py](analyzer.py)  
- Frontend React (Vite): [frontend/src/App.jsx](frontend/src/App.jsx), [frontend/src/main.jsx](frontend/src/main.jsx) — [frontend/package.json](frontend/package.json)  
- Tests rápidos: [tests.py](tests.py)  
- Dependencias: [requirements.txt](requirements.txt)


## Requisitos
- Python 3.8+
- npm (para frontend)
- Instalar dependencias Python:
  ```sh
  python -m venv .venv
  .venv\Scripts\activate    
  pip install -r requirements.txt


## Ejecutar backend (API)
Activar el entorno Python (ver arriba).
Ejecutar:
El servidor Flask se ejecuta en http://localhost:5000 y expone la ruta /api/status.

## Ejecutar frontend (desarrollo)
Abrir terminal en la carpeta frontend:
Abrir la URL que Vite muestre (por defecto http://localhost:5173). El frontend consulta http://localhost:5000/api/status.
Nota: si el navegador bloquea la petición por CORS

3. Reporte breve
- Decisiones de diseño tomadas
  - Simplicidad primero: el controlador principal es [`sdn_controller.SimpleSDNController`](sdn_controller.py) y mantiene estructuras sencillas (diccionarios para hosts/routers y un `deque` para historial) para facilitar simulación y prueba rápida.
  - Ventana temporal para detección: la detección de ataques usa una ventana de tiempo (`window_seconds` en [`sdn_controller.SimpleSDNController`](sdn_controller.py)) y un umbral (`attack_threshold`) para evitar falsos positivos por picos momentáneos.
  - Separación de responsabilidades: generación y simulación de tráfico está en `main.py` (clase `NetworkSimulator`) mientras que el análisis está en [`analyzer.TrafficAnalyzer`](analyzer.py). Esto permite probar componentes por separado.
  - Tipos explícitos de tráfico: el enum [`network.TrafficType`](network.py) centraliza categorías de paquetes (WEB, VIDEO, ATTACK, etc.) facilitando reglas basadas en tipo.
  - Frontend liviano: la UI en [frontend/src/App.jsx](frontend/src/App.jsx) consulta la API REST en [main.py](main.py) para mostrar estado sin lógica de control compleja en el cliente.

- Problemas encontrados y soluciones
  - Problema: conteo ineficiente en ventanas temporales si el historial crece mucho.
    - Solución: usar `collections.deque` con `maxlen` y limitar la ventana de conteo para reducir trabajo; además considerar indexar por host si escala.
  - Problema: detección por simple conteo puede bloquear hosts válidos (falsos positivos).
    - Solución: introducir roles en [`network.Host`](network.py) y excepciones por rol; ajustar `attack_threshold` y `window_seconds` según métricas reales; agregar heurísticas por tipo de tráfico (usar [`network.TrafficType`](network.py)).
  - Problema: bloqueo de hosts no persistente entre reinicios.
    - Solución: si se necesita persistencia, guardar estado en disco o base de datos desde [`sdn_controller.SimpleSDNController`](sdn_controller.py).
  - Problema: peticiones CORS entre frontend y backend durante desarrollo.
    - Solución: habilitar CORS en Flask en [main.py](main.py) o usar proxy en Vite ([frontend/vite.config.js](frontend/vite.config.js)).
  - Problema: visualización simple en [`analyzer.TrafficAnalyzer`](analyzer.py) requiere entorno gráfico.
    - Solución: soportar salida a archivo (PNG) o exportar datos para dashboards si se ejecuta en servidor sin GUI.
