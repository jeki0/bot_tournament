#!/usr/bin/env python

# Bot tournament server -

import asyncio
import websockets
import json
import threading
import time

USERS = set()
game_data = {
    'point': {
        'x': 100,
        'y': 50,
        'mx': -0.1,
        'my': 0.1,
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
match = {}
bots = 0
point_speed = 30


async def add_user(websocket, first_data):
    """ Добавление нового пользователя в массив """
    USERS.add(websocket)
    # if first_data['type'] == 'bot':
    #     match[websocket] = 0
    #     print('bot')
    # if first_data['type'] == 'bot':
    #     match[websocket] = 1
    #     print('bot')
    if first_data['type'] == 'site':
        print('site')


async def remove_user(websocket):
    """ Если юзер ливнул то удаляем его """
    USERS.remove(websocket)


def get_data_json():
    """ Данные пихаем в json и возвращаем их """
    return json.dumps(game_data)


def timer():
    """ Таймер в отдельном потоке, обновление данных и отправка"""
    while True:
        update_point()
        if USERS:
            for user in USERS:
                asyncio.run(user.send(get_data_json()))
        time.sleep(0.02)


def get_first_data(first_data):
    return json.loads(first_data)


def update_point():
    if game_data['point']['my'] < 0:
        if game_data['point']['y'] < 0:
            game_data['point']['my'] = game_data['point']['my'] * -1
    if game_data['point']['my'] > 0:
        if game_data['point']['y'] > 790:
            game_data['point']['my'] = game_data['point']['my'] * -1

    p_y = game_data['point']['y'] + (point_speed* game_data['point']['my'])
    p_x = game_data['point']['x'] + (point_speed * game_data['point']['mx'])

    for user in game_data['users']:
        if p_y > user['y'] and p_y < (user['y'] + 30):
            if p_x > user['x'] and p_x < (user['x'] + 10):
                game_data['point']['mx'] = game_data['point']['mx'] * -1

    game_data['point']['y'] = game_data['point']['y'] + (point_speed * game_data['point']['my'])
    game_data['point']['x'] = game_data['point']['x'] + (point_speed * game_data['point']['mx'])

    if game_data['point']['x'] < -10:
        game_data['point']['x'] = 500
    if game_data['point']['x'] > 1010:
        game_data['point']['x'] = 400

    for user in game_data['users']:
        if user['v'] == 'up':
            if user['y'] > 0:
                user['y'] -= 4
        if user['v'] == 'down':
            if user['y'] < 790:
                user['y'] += 4


def update_user(data, websocket):
    game_data['users'][data['from']]['v'] = data['command']


async def connect(websocket, path):
    """ Работаем с новым подключением """
    print('Connected')
    first_data_json = await websocket.recv()
    first_data = get_first_data(first_data_json)
    await add_user(websocket, first_data)
    try:
        await websocket.send(get_data_json())
        async for message in websocket:
            data = json.loads(message)
            update_user(data, websocket)
    finally:
        await remove_user(websocket)

start_server = websockets.serve(connect, "localhost", 8080)

x = threading.Thread(target=timer, args=())
x.start()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()