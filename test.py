#!/usr/bin/env python3
import time

import json
import paho.mqtt.client as mqtt
import config

client = mqtt.Client()
client.connect('localhost')
client.subscribe("middles")


#camera is offsetted from the sucktion cup
cam_offset_x=50
height=config.cam_z

middles=[]
def handler(client,user_data, message):
    global middles
    middles=json.loads(message.payload.decode())
    # print(middles)

client.on_message=handler

client.loop_start()

from dobotfun.dobotfun import DobotFun
import pydobot
from pydobot.dobot import Position


robot=DobotFun()

tarres_x={}
tarres_y={}
factors_x={}
factors_y={}


def save():
    with open('cam.cal','w') as fh:

        json.dump({
            'tarres_x': tarres_x,
            'tarres_y': tarres_y,
            'factors_x': factors_x,
            'factors_y': factors_y
        },fh)


def load():
    global tarres_x
    global tarrex_y
    global factors_y
    global factors_x
    with open('cam.cal','r') as fh:
        obj=json.load(fh)

        tarres_x=obj['tarres_x']
        tarres_y=obj['tarres_y']
        factors_x=obj['factors_x']
        factors_y=obj['factors_y']


def wait_cam():
    time.sleep(3)


def do_tarre(z):
    robot.move_to(config.middle.x, config.middle.y, z)
    wait_cam()

    if len(middles)!=1:
        raise(Exception("Only one object please"))

    #cam x and y and robot x and y are swapped (x=y)
    tarres_x[z]=middles[0][1]
    tarres_y[z]=middles[0][0]

def do_calibrate_x(offset_x, z):
    robot.move_to(config.middle.x+offset_x, config.middle.y, z)
    wait_cam()

    if len(middles)!=1:
        raise(Exception("Only one object please"))

    cam_x=middles[0][1]

    cam_offset_x=tarres_x[z]-cam_x

    #calculate robot pixels per cam pixel:
    factors_x[z]=(offset_x/cam_offset_x)

    print(f"Cal factor X @{z}: offset={cam_offset_x} factors={factors_x[z]}")

def do_calibrate_y(offset_y, z):
    robot.move_to(config.middle.x , config.middle.y+offset_y, z)
    wait_cam()

    if len(middles)!=1:
        raise(Exception("Only one object please"))

    cam_y=middles[0][0]

    cam_offset_y=tarres_y[z]-cam_y

    #calculate robot pixels per cam pixel:
    factors_y[z]=(offset_y / cam_offset_y)

    print(f"Cal factor Y @{z}: offset={cam_offset_y} factors={factors_y[z]}")



def point_middle_cam():
    robot.move_to(config.middle.x, config.middle.y, config.point_z)


def recal():

    robot.home()
    point_middle_cam()
    print("MAKE SURE THE BLOCK IS IN THE MIDDLE OF THE CAM, press enter.")
    input()
    do_tarre(height)
    do_calibrate_x(-30, height)
    do_calibrate_y(30, height)

    save()

def goto_cam_home():
    robot.move_to(config.middle.x, config.middle.y, height)

#return robot x,y coord of object
def cam_to_robot(cam_x, cam_y, z=height):

    cam_offset_x=tarres_x[z]-cam_x
    cam_offset_y=tarres_y[z]-cam_y

    offset_x=factors_x[z]*cam_offset_x
    offset_y=factors_y[z]*cam_offset_y

    print(offset_x, offset_y)

load()

recal()

goto_cam_home()
wait_cam()
cam_to_robot(middles[0][1], middles[0][0])

