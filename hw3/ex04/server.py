# Server code 
import asyncio
import websockets
 
# create handler for each connection
async def handler(websocket, path):
    cnt = 10000
    data = await websocket.recv()
    print("Server Received Message",path,data) # receive message from client
    async for msg in websocket:
       msg = 'GotClientmMessage:' + msg
       print( msg) # print out client message
       msg = 'ServerNewMessage' + str(cnt) # construct a server message
       cnt += 1
       await websocket.send(msg) # send back to client
 
start_server = websockets.serve(handler, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()