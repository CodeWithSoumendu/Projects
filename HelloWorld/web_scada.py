import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from asyncua import Client

app = FastAPI()
active_connections = []
opc_nodes = {}  # Store nodes globally so the websocket can trigger writes

async def opc_client_loop():
    """Background task to poll OPC UA server and broadcast to web clients."""
    url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
    
    while True:
        try:
            print("Attempting to connect to OPC UA Server...")
            async with Client(url=url) as client:
                print("Connected to OPC UA Server!")
                uri = "http://my_custom_plc.local"
                idx = await client.get_namespace_index(uri)
                
                opc_nodes['temp'] = await client.nodes.objects.get_child([f"{idx}:MachineData", f"{idx}:Temperature"])
                opc_nodes['press'] = await client.nodes.objects.get_child([f"{idx}:MachineData", f"{idx}:Pressure"])
                opc_nodes['motor'] = await client.nodes.objects.get_child([f"{idx}:MachineData", f"{idx}:MotorRunning"])
                
                while True:
                    # Read values
                    temp = await opc_nodes['temp'].read_value()
                    press = await opc_nodes['press'].read_value()
                    motor = await opc_nodes['motor'].read_value()
                    
                    # Package data as JSON
                    data = json.dumps({"temperature": temp, "pressure": press, "motor": motor})
                    
                    # Broadcast to all open web browsers
                    for connection in active_connections:
                        await connection.send_text(data)
                        
                    await asyncio.sleep(0.1) # 100ms update rate
                    
        except Exception as e:
            print(f"OPC Connection lost. Retrying in 2 seconds... Error: {e}")
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    # Start the OPC UA polling loop in the background when the web server starts
    asyncio.create_task(opc_client_loop())

@app.get("/")
async def get():
    # Serve the HTML frontend
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Listen for messages from the browser (e.g., button clicks)
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            if msg.get("command") == "toggle_motor" and 'motor' in opc_nodes:
                current_state = await opc_nodes['motor'].read_value()
                # Write the inverse state to the PLC
                await opc_nodes['motor'].write_value(not current_state)
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    # Run the web server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)