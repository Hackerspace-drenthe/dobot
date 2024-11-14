#!/usr/bin/env python3
import time

import json
import paho.mqtt.client as mqtt
import config

client = mqtt.Client()
client.connect('localhost')
client.subscribe("middles")

height = config.cam_z

middles = []

stable_count=0
last_x=-1
last_y=-1

stable_max_offset=3
frame_skip=0

def reset_cam():
    global stable_count
    global frame_skip

    stable_count=3
    frame_skip=8 #cam lag

def handler(client, user_data, message):
    global middles
    middles = json.loads(message.payload.decode())
    # print(middles)

    global stable_count
    global last_x
    global last_y

    global frame_skip
    if frame_skip>0:
        frame_skip=frame_skip-1
        print(f"Waiting for cam: {frame_skip}")
        return

    if len(middles)==0:
        stable_count=4
    else:
        if abs(last_x-middles[0][0])<=3 and abs(last_y-middles[0][1])<=3:
            if stable_count>0:
               stable_count=stable_count-1
               print(f"Waiting for stable: {stable_count}")
        else:
            stable_count=4

        last_x=middles[0][0]
        last_y=middles[0][1]


client.on_message = handler

client.loop_start()

from dobotfun.dobotfun import DobotFun
import pydobot
from pydobot.dobot import Position

robot = DobotFun()

tarres_x = 0
tarres_y = 0
factors_x = 0
factors_y = 0


def save():
    with open('cam.cal', 'w') as fh:
        json.dump({
            'tarres_x': tarres_x,
            'tarres_y': tarres_y,
            'factors_x': factors_x,
            'factors_y': factors_y
        }, fh)


def load():
    global tarres_x
    global tarres_y
    global factors_y
    global factors_x
    with open('cam.cal', 'r') as fh:
        obj = json.load(fh)

        tarres_x = obj['tarres_x']
        tarres_y = obj['tarres_y']
        factors_x = obj['factors_x']
        factors_y = obj['factors_y']


cam_lag=1

def wait_cam():

    #cam lag
    # time.sleep(0)
    # global stable_count
    # stable_count=0

    while stable_count>0:
        time.sleep(0.1)


def do_tarre():
    global tarres_x
    global tarres_y

    robot.move_to(config.middle.x, config.middle.y, height)
    wait_cam()

    if len(middles) != 1:
        raise (Exception("Only one object please"))

    # cam x and y and robot x and y are swapped (x=y)
    tarres_x = middles[0][1]
    tarres_y = middles[0][0]


def do_calibrate_x(offset_x):
    global tarres_x
    global factors_x
    robot.move_to(config.middle.x + offset_x, config.middle.y, height)
    wait_cam()

    if len(middles) != 1:
        raise (Exception("Only one object please"))

    cam_x = middles[0][1]

    cam_offset_x = tarres_x - cam_x

    # calculate robot pixels per cam pixel:
    factors_x = (offset_x / cam_offset_x)

    print(f"Cal factor X: offset={cam_offset_x} factors={factors_x}")


def do_calibrate_y(offset_y):
    global factors_y

    robot.move_to(config.middle.x, config.middle.y + offset_y, height)
    wait_cam()

    if len(middles) != 1:
        raise (Exception("Only one object please"))

    cam_y = middles[0][0]

    cam_offset_y = tarres_y - cam_y

    # calculate robot pixels per cam pixel:
    factors_y = (offset_y / cam_offset_y)

    print(f"Cal factor Y: offset={cam_offset_y} factors={factors_y}")


def point_middle_cam():
    robot.move_to(config.middle.x, config.middle.y, config.point_z)


def recal():
    robot.home()
    point_middle_cam()
    print("MAKE SURE THE BLOCK IS IN THE MIDDLE OF THE CAM, press enter.")
    input()
    do_tarre()
    do_calibrate_x(-30)
    do_calibrate_y(30)

    save()


def goto_cam_home():
    robot.move_to(config.middle.x, config.middle.y, height, 90)


# return robot x,y coord of object
def cam_to_robot(cam_x, cam_y):
    cam_offset_x = tarres_x - cam_x
    cam_offset_y = tarres_y - cam_y

    # relative tov cam home
    offset_x = factors_x * cam_offset_x
    offset_y = factors_y * cam_offset_y

    # absolute
    x = config.middle.x - offset_x + config.cam_offset_x
    y = config.middle.y - offset_y

    return(x,y)


# recal()
load()


while True:
    goto_cam_home()
    wait_cam()
    (x,y)=cam_to_robot(middles[0][1], middles[0][0])
    reset_cam()
    robot.move_to(x,y,config.point_z, 90)
    robot.vast()
    robot.move_to(x,y, config.point_z+80, 90)
    robot.move_to(150,150, config.point_z+80, 90)
    robot.los()


