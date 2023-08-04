import secu
import json
import asyncio
import websockets
import requests

status = "online"
token = secu.token

headers = {"Authorization": token, "Content-Type": "application/json"}
userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
disc= userinfo["discriminator"]
userid = userinfo["id"]

if  disc == 0 :
    disc = ""
else :
    disc= userinfo["discriminator"]

async def keep_online(token, status):
    async with websockets.connect('wss://gateway.discord.gg/?v=9&encoding=json') as ws:
        start = json.loads(await ws.recv())
        heartbeat = start['d']['heartbeat_interval']
        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "Windows 11",
                    "$browser": "Google Chrome",
                    "$device": "Windows"
                },
                "presence": {
                    "status": status,
                    "afk": True
                }
            },
            "s": None,
            "t": None
        }
        await ws.send(json.dumps(auth))
        online = {"op": 1, "d": "None"}
        await asyncio.sleep(heartbeat / 1000)
        await ws.send(json.dumps(online))

async def run_keep_online():
    print(f"Logged in as @{username} ({userid}).")
    while True:
        await keep_online(token, status)
        await asyncio.sleep(30)

asyncio.run(run_keep_online())
