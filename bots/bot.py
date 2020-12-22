import asyncio
import websockets
import json


async def hello():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"type":"bot0"}')
        async for message in websocket:
            data = json.loads(message)
            """ Здесь тело бота. Данные полученные с серевера хранятся в объекте data
            {
                'point': {
                    'x': 100,
                    'y': 100,
                    'mx': 0.01,
                    'my': 0.01,
                },
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

            if data['point']['y'] > data['users'][0]['y'] + 5:
                send_data = 'down'

            if data['point']['y'] < data['users'][0]['y'] + 25:
                send_data = 'up'

            """ Конец тела бота. для отпрвки вниз или вверх нужну в send_data указать down или up """
            json_out = json.dumps({'command': send_data, 'from': 0})
            await websocket.send(json_out)

asyncio.get_event_loop().run_until_complete(hello())