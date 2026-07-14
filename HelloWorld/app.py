import asyncio
from asyncua import Server, ua

async def main():
    #1 initialze the server

    server=Server()
    await server.init()

    #2 set the endpoint(0.0.0.0 allows any device on the network to connect
    #standard opc ua port is 4840)

    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    3# setup a namespace(A unique indentifier for tags)
    uri="http://my_custom_plc.local"
    idx= await server.register_namespace(uri)

    #4 create an object (siemens data block or tag group)
    my_data_block = await server.nodes.objects.add_object(idx,"MachineData")

    #5 add variable tags to the object
    #add variable(namespace_index,tagname, initial value)

    temperatue= await my_data_block.add_variable(idx,"Temperature",25.5)
    pressure= await my_data_block.add_variable(idx,"Pressure",100.0)
    motor_running= await my_data_block.add_variable(idx,"MotorRunning",False)

    #6 make tags writtable by other PLCs

    await temperatue.set_writable()
    await pressure.set_writable()
    await motor_running.set_writable()

    print("OPC UA server started at opc.tcp://0.0.0.0:4840")
    print("Waiting for clients on ethernet network")

    #7 start the server and simulate changing data
    async with server:
        while True:
            current_temp= await temperatue.read_value()
            new_temp= current_temp+0.5

            if new_temp>50.0:
                new_temp=25.5

            await temperatue.write_value(new_temp)
            await asyncio.sleep(1)
if __name__=="__main__":

    asyncio.run(main())
                                        
                                        