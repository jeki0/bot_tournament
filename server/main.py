#!/usr/bin/env python

# Bot tournament server -

import asyncio
import websockets
import json
import threading
import time
import random

USERS = set()
game_data = {
    'points': [],
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


def add_points():
    for i in range(10):
        game_data['points'].append({
            'x': random.randint(100, 900),
            'y': random.randint(100, 700),
            'mx': -0.1,
            'my': 0.1,
        })


add_points()


async def add_user(websocket, first_data):
    """ Добавление нового пользователя в массив """
    USERS.add(websocket)
    print('New connect:')
    if first_data['type'] == 'site':
        print('Site')
    else:
        print('Bot')


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
            users_temp = USERS
            for user in users_temp:
                asyncio.run(user.send(get_data_json()))
                print(game_data['points'][0]['x'])
        time.sleep(0.1)


def get_first_data(first_data):
    return json.loads(first_data)


def update_point():
    """ Обновление позции точек и палок """
    for point in game_data['points']:
        if point['my'] < 0:
            if point['y'] < 0:
                point['my'] = point['my'] * -1
        if point['my'] > 0:
            if point['y'] > 790:
                point['my'] = point['my'] * -1

        p_y = point['y'] + (point_speed * point['my'])
        p_x = point['x'] + (point_speed * point['mx'])

        for user in game_data['users']:
            if p_y > user['y'] and p_y < (user['y'] + 30):
                if p_x > user['x'] and p_x < (user['x'] + 10):
                    point['mx'] = point['mx'] * -1

        point['y'] = point['y'] + (point_speed * point['my'])
        point['x'] = point['x'] + (point_speed * point['mx'])

        if point['x'] < -10:
            point['y'] = random.randint(50, 700)
            point['x'] = 500
        if point['x'] > 1010:
            point['x'] = 500
            point['x'] = 500
            point['y'] = random.randint(50, 700)

    for user in game_data['users']:
        if user['v'] == 'up':
            if user['y'] > 0:
                user['y'] -= 4
        if user['v'] == 'down':
            if user['y'] < 790:
                user['y'] += 4


def update_user(data, websocket):
    """ Смена вектора бота """
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

start_server = websockets.serve(connect, "localhost", 3000)

x = threading.Thread(target=timer, args=())
x.start()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()