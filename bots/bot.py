import asyncio
import websockets
import json

i = 0

async def hello():
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"type":"bot0"}')
        async for message in websocket:
            data = json.loads(message)
            """ Здесь тело бота. Данные полученные с серевера хранятся в объекте data
            {
                'points': [
                    {
                        'x': 500,
                        'y': 50,
                        'mx': -0.1,
                        'my': 0.1,
                    },
                    {
                        'x': 500,
                        'y': 100,
                        'mx': 0.1,
                        'my': 0.1,
                    },
                    {
                        'x': 500,
                        'y': 400,
                        'mx': -0.1,
                        'my': 0.1,
                    }
                ],
                'users': [
                    {
                        'x': 0,
                        'y': 0,
                        'v': 0,
                    },
                    {
                        'x': 990,
                        'y': 0,
                        'v': 0,
                    }
                ]
            }
            """
            print(i)

            send_data = 'down'
            """ Конец тела бота. для отпрвки вниз или вверх нужну в send_data указать down или up """
            json_out = json.dumps({'command': send_data, 'from': 0})
            await websocket.send(json_out)

asyncio.get_event_loop().run_until_complete(hello())