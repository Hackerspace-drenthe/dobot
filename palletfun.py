import sys
import os
import logging
from serial.tools import list_ports
import time

sys.path.insert(0, os.path.abspath('pydobot'))

from time import sleep, time

from pydobot import Dobot



logging.Logger("Dobot", logging.DEBUG)

port = list_ports.comports()[0].device
device = Dobot(port=port)

suck_delay=1
#     <--- Y + -->
#  ^  LB      RB
#  |
#  X                 RIJ
#  +                 RIJ
#  V  LO      RO     RIJ
#
#   KOL    KOL   KOL

# links boven
# pallet_lb=( -4.6, -270.0,-48.4 )
Xnn = -4.6
Ynn = -270

# rechts boven
# pallet_rb=( -7.4, -195.0,-43.4 )
Xn1 = -7.4
Yn1 = -195.0

# links onder
# pallet_lo=( 70.9, -268.5,-46.2 )
X1n = 70.9
Y1n = -268.5

# rechts onder
# pallet_ro=( 67.5, -195.1,-47.3 )
X11 = 65.5
Y11 = -195.1

# hoeveel x hoeveel blokken is de pallet?
pallet_grid = 4

grond_z = -47

blok_size = 25

pallet_filled = [True] * (pallet_grid * pallet_grid)


pallet_aanwezig=[
    (1,1),
    (1,2),
    (2,1),
    (1,3),
    (2,2),
    (3,1),
    (1,4),
    (2,3),
    (3,2),
    (4,1),
    (2,4),
    (3,3),
    (4,2),
    (3,4),
    (4,3),
    (4,4)
]

pallet_in_gebruik=[]

locaties=[]

def calc_pallet(r, k):
    # y = Y11 + (( Yn1 -  Y11)/(pallet_grid-1)) * (r-1) + (( Y1n - Y11 )/(pallet_grid-1)) * (k-1)
    # x = X11 + (( Xn1 -  X11)/(pallet_grid-1)) * (r-1) + (( X1n - X11 )/(pallet_grid-1)) * (k-1)

    # y = Y11 + (( Y11 - Yn1)/(pallet_grid-1)) * (r-1) + (( Y11  - Y1n )/(pallet_grid-1)) * (k-1)
    # x = X11 + (( X11 - Xn1 )/(pallet_grid-1)) * (r-1) + (( X11  - X1n )/(pallet_grid-1)) * (k-1)

    x_comp = ((Yn1 - Y11) / (pallet_grid - 1)) * (r - 1)
    y = Y11 + ((Y1n - Y11) / (pallet_grid - 1)) * (k - 1) + x_comp

    y_comp = ((X1n - X11) / (pallet_grid - 1)) * (k - 1)
    x = X11 + ((Xn1 - X11) / (pallet_grid - 1)) * (r - 1) + y_comp

    # x=pallet_lb[0] + (((pallet_ro[0]-pallet_lb[0])/(pallet_grid-1)) * (r-1))
    # y=pallet_lb[1] + (((pallet_ro[1]-pallet_lb[1])/(pallet_grid-1)) * (k-1))
    return (x, y)

def pak_pallet(r,k):
    (x,y)=calc_pallet(r,k)
    device.move_to(x,y,grond_z+50)
    device.move_to(x,y,grond_z)
    device.wait_for_cmd(device.suck(True))
    sleep(suck_delay)
    device.move_to(x+5,y+5,grond_z+50)

def zet_pallet(r,k):
    (x,y)=calc_pallet(r,k)
    device.move_to(x+5, y+5, grond_z +50)
    device.move_to(x+5, y+5, grond_z )
    device.speed(10,10)
    device.move_to(x, y, grond_z )
    device.wait_for_cmd(device.suck(False))
    device.wait_for_cmd(device.move_to(x-1, y-1, grond_z))
    device.speed(100,100)
    sleep(suck_delay)
    device.wait_for_cmd(device.move_to(x, y, grond_z+50))

def zet(x,y,z):
    device.move_to(x,y,z+30)
    device.move_to(x,y,z)
    device.wait_for_cmd(device.suck(False))
    sleep(suck_delay)
    device.speed(10,10)
    device.move_to(x,y,z+30)
    device.speed(100,100)
    locaties.insert(0, (x,y,z ) )

def cleanup():
    for locatie in locaties:
        pak(locatie[0], locatie[1], locatie[2])
        zet_pallet_volgende()
    locaties.clear()

def pak(x,y,z):
    device.move_to(x,y,z+30)
    device.move_to(x,y,z)
    device.wait_for_cmd(device.suck(True))
    sleep(suck_delay)
    device.move_to(x,y,z+30)

def pak_pallet_volgende():
    (r,k)=pallet_aanwezig.pop(0)
    pallet_in_gebruik.insert(0, (r,k)  )
    pak_pallet(r,k)

def zet_pallet_volgende():
    (r, k) = pallet_in_gebruik.pop(0)
    pallet_aanwezig.insert(0, (r,k ) )
    zet_pallet(r, k)



for nr in range(0,3):
    pak_pallet_volgende()
    zet( 240- int(nr/8)*40, (nr%8)*40 + (-120), grond_z  )

locaties.reverse()


cleanup()

