#!/usr/bin/env python
import signal
import sys

from dobotfun.dobotfun import DobotFun

from dobotfun.palletfun import PalletFun
from tictactoe import *

# def interrupted(signum, frame):
#     "called when read times out"
#     print ('interrupted!')
#
# signal.signal(signal.SIGALRM, interrupted)
# signal.alarm(3)


import readchar

dobot = DobotFun()
pallet = PalletFun(dobot)

block_size = 28
x_start = 135
y_start = -45
optil_z = pallet.pallet_config.z + block_size + 10


def calc_grid_positie(r, k):
    return (x_start + (r * block_size), y_start + (k * block_size))


def bestuur_positie( r,k ):
    print("Gebruikt pijltjes toetsen om een locatie te kiezen:")
    while True:
        (x,y)=calc_grid_positie( r, k )
        dobot.move_to_nowait( x,y, optil_z )

        key = readchar.readkey()
        if key == readchar.key.ENTER:
            return ( r,k )
        elif key == readchar.key.RIGHT:
            k = k + 1
        elif key == readchar.key.LEFT:
            k = k - 1
        elif key == readchar.key.UP:
            r = r - 1
        elif key == readchar.key.DOWN:
            r = r + 1
        elif key == 'q':
            print("QUIT")
            sys.exit(0)

        #limiteer bereik
        r=max(-2,r)
        r=min(4,r)
        k=max(-2,k)
        k=min(4,k)


try:
    real_raw_input = raw_input
except NameError:
    real_raw_input = input

board, winner = EMPTY_BOARD, None
chance_for_error = 0.0

print("Input the col and row number separated by a comma.")
print("e.g., to tick the middle cell in the top row ?> 2, 1")

while winner is None:
    print(get_printable_board(board))
    pallet.pak_pallet_volgende()

    r=0
    k=0
    while True:
        try:
            (r,k)=bestuur_positie(r,k)
            board, winner = play(board, 'X', k, r)

            #gelukt, plaats blokje
            ( x,y )= calc_grid_positie(r,k)
            pallet.zet(x,y)

            break
        except (IllegalMove, ValueError):
            #ongeldige move, schud nee
            ( x,y )= calc_grid_positie(r,k)
            dobot.move_to(x,y+3, optil_z)
            dobot.move_to(x,y, optil_z)
            dobot.move_to(x,y+3, optil_z)

        except KeyboardInterrupt:
            exit()

    if winner is None:
        pallet.pak_pallet_volgende()
        (k, r) = minimax(board, 'O')
        (x, y) = calc_grid_positie(r, k)
        pallet.zet(x, y)
        board, winner = play(board, 'O', k, r)

print(get_printable_board(board))
if winner == 'T':
    print("Tie!")
else:
    print("%s is the winner!" % winner)
