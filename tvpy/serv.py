import asyncio
from websockets import serve  # type: ignore


async def echo(websocket):
    async for msg in websocket:
        print('Got', msg)
        await websocket.send(msg)


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
