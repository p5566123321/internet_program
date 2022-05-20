import asyncio
import datetime
import random
import websockets
import requests 
import numpy as np
import json

url="https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
async def time(websocket, path):
    while True:
        r = requests.get(url).json()
        
        #for x in range (np.size(r)):
        #    sna=r[x]['sna']
        #now = datetime.datetime.utcnow().isoformat() + 'Z'
        #datas = [r,now]
        #print(type(json.dumps(r)))
        await websocket.send(json.dumps(r))
        await asyncio.sleep(random.random() * 12)

start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()