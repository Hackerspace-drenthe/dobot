#GPL3.0 - (c)edwin@datux.nl

import sys
import os
import logging
from serial.tools import list_ports
import time

sys.path.insert(0, os.path.abspath('pydobot'))

from time import sleep, time

from pydobot import Dobot

suck_delay = 1

# links boven
Xlb = -4.6
Ylb = -270

# rechts boven
Xrb = -7.4
Yrb = -195.0

# links onder
Xlo = 70.9
Ylo = -268.5

# rechts onder
Xro = 65.5
Yro = -195.1

# hoeveel x hoeveel blokken is de pallet?
pallet_grid = 4

grond_z = -47

blok_size = 25

pallet_filled = [True] * (pallet_grid * pallet_grid)

pallet_aanwezig = [
    (1, 1),
    (1, 2),
    (2, 1),
    (1, 3),
    (2, 2),
    (3, 1),
    (1, 4),
    (2, 3),
    (3, 2),
    (4, 1),
    (2, 4),
    (3, 3),
    (4, 2),
    (3, 4),
    (4, 3),
    (4, 4)
]

pallet_in_gebruik = []

locaties = []


#     <--- Y + -->
#  ^  lb      rb
#  |
#  X                 RIJ
#  +                 RIJ
#  V  lo      ro     RIJ
#
#   KOL    KOL   KOL  1,1

def calc_pallet(r, k):
    x_factor = (r - 1) / (pallet_grid - 1)
    y_factor = (k - 1) / (pallet_grid - 1)

    x = Xro * (1 - x_factor) * (1 - y_factor) + Xlo * (1 - x_factor) * y_factor + Xrb * x_factor * (1 - y_factor) + Xlb * x_factor * y_factor
    y = Yro * (1 - x_factor) * (1 - y_factor) + Ylo * (1 - x_factor) * y_factor + Yrb * x_factor * (1 - y_factor) + Ylb * x_factor * y_factor

    return (x, y)


def pak_pallet(r, k):
    (x, y) = calc_pallet(r, k)
    device.move_to(x, y, grond_z + 50)
    device.move_to(x, y, grond_z)
    device.wait_for_cmd(device.suck(True))
    sleep(suck_delay)
    device.move_to(x + 5, y + 5, grond_z + 50)


def zet_pallet(r, k):
    (x, y) = calc_pallet(r, k)
    device.move_to(x + 5, y + 5, grond_z + 50)
    device.move_to(x + 5, y + 5, grond_z)
    device.speed(10, 10)
    device.move_to(x, y, grond_z)
    device.wait_for_cmd(device.suck(False))
    device.wait_for_cmd(device.move_to(x - 1, y - 1, grond_z))
    device.speed(100, 100)
    sleep(suck_delay)
    device.wait_for_cmd(device.move_to(x, y, grond_z + 50))


def zet(x, y, z):
    device.move_to(x, y, z + 30)
    device.move_to(x, y, z)
    device.wait_for_cmd(device.suck(False))
    sleep(suck_delay)
    device.speed(10, 10)
    device.move_to(x, y, z + 30)
    device.speed(100, 100)
    locaties.insert(0, (x, y, z))


def cleanup():
    for locatie in locaties:
        pak(locatie[0], locatie[1], locatie[2])
        zet_pallet_volgende()
    locaties.clear()


def pak(x, y, z):
    device.move_to(x, y, z + 30)
    device.move_to(x, y, z)
    device.wait_for_cmd(device.suck(True))
    sleep(suck_delay)
    device.move_to(x, y, z + 30)


def pak_pallet_volgende():
    (r, k) = pallet_aanwezig.pop(0)
    pallet_in_gebruik.insert(0, (r, k))
    pak_pallet(r, k)


def zet_pallet_volgende():
    (r, k) = pallet_in_gebruik.pop(0)
    pallet_aanwezig.insert(0, (r, k))
    zet_pallet(r, k)


print("Pallet coords:")
for r in reversed(range(1, 5)):
    for k in reversed(range(1, 5)):
        (x, y) = calc_pallet(r, k)
        print(f"{x:.1f},{y:.1f}\t", end='')
        # print(f"{r},{k}\t", end='')
    print()

logging.Logger("Dobot", logging.DEBUG)

port = list_ports.comports()[0].device
device = Dobot(port=port)

for nr in range(0, 3):
    pak_pallet_volgende()
    zet(240 - int(nr / 8) * 40, (nr % 8) * 40 + (-120), grond_z)

locaties.reverse()

cleanup()
