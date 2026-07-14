# Python Web-Based Industrial SCADA

A real-time, web-based SCADA (Supervisory Control and Data Acquisition) dashboard built with Python. This system bridges industrial OPC UA protocols with a modern web interface.

## Features
*   **Real-time Monitoring:** Live temperature and pressure data streaming via WebSockets.
*   **Remote Control:** Bi-directional communication to toggle motor states.
*   **Modern UI:** Dark-themed dashboard with animated indicators built with Tailwind CSS.
*   **Backend Architecture:** Powered by FastAPI for asynchronous performance.

## Prerequisites
You will need Python 3.12+ installed.
Install the required libraries:
```bash
pip install fastapi uvicorn websockets asyncua

python app.py
python web_scada.py
