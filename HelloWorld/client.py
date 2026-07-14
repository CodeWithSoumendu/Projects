import asyncio
from asyncua import Client

async def main():
    #1 set url of the server
    #127.0.0.1 means this exact computer
    #if running on a diiferent pc then replace with laptops wifi or ethernet ip.

    url="opc.tcp://127.0.0.1:4840/freeopcua/server/"
    print("connecting to OPC UA Server at {url}....")

    #2. connect with the server
    # 'async with' is great because it automatically disconnects when script finishes
    async with Client(url=url) as client:
        print("Successfully Connected!")

        #3 Find our spacific Namespace

        uri="http://my_custom_plc.local"
        idx=await client.get_namespace_index(uri)

        #4 Locate the tags(nodes) using their browse path
        #We look inside the objects folder ->MachineDataFolder->Specific tag

        temperature_node=await client.nodes.objects.get_child([f"{idx}:MachineData",f"{idx}:Temperature"])
        pressure_node=await client.nodes.objects.get_child([f"{idx}:MachineData",f"{idx}:Pressure"])
        motor_node=await client.nodes.objects.get_child([f"{idx}:MachineData",f"{idx}:MotorRunning"])

        #5. read value from the server

        current_temp= await temperature_node.read_value()
        print(f"Live temperature is :{current_temp}")

        current_pressure= await pressure_node.read_value()
        print(f"Live pressure is :{current_pressure}")

        current_motor= await motor_node.read_value()
        print(f"Motor state before writing: {current_motor}")

        #6 Write the value to the server(Turn motor on)
        print("Sending command to turn motor ON....")
        await motor_node.write_value(True)

        #7 read again to verify if it was successful

        new_motor =await motor_node.read_value()
        print(f"Motor state after writting :{new_motor}")

if __name__=="__main__":
    asyncio.run(main())