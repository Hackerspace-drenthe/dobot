#!/usr/bin/env python
import signal
import sys
from time import sleep

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

dobot = DobotFun(port=None, id="WOPR")
dobot.log.show_debug=False
pallet = PalletFun(dobot)

block_size = 29
x_start = 135
y_start = -45
optil_z = pallet.pallet_config.z + block_size + 10


def calc_grid_positie(r, k):
    return (x_start + (r * block_size), y_start + (k * block_size))

def sad():
    # :( verloren
    dobot.move_to(156, -211, pallet.pallet_config.z)
    dobot.speed(5,1)
    dobot.move_to(156, -211, pallet.pallet_config.z-10)
    dobot.snel()

def happy():
    # :)  gewonnne \o/
    dobot.move_to(165, 0, 160)
    dobot.move_to(165, 0, 160)
    dobot.move_to(165, 0, 140)
    dobot.move_to(165, 0, 160)
    dobot.move_to(165, 0, 140)
    dobot.move_to(165, 0, 160)
    dobot.move_to(165, 0, 140)
    dobot.snel()



demo=True

def bestuur_positie( r,k ):
    """laat de player een positie kiezen met pijltjes"""

    global demo
    if demo:

        dobot.verbose("SHALL WE PLAY A GAME?")
        i, o, e = select.select([sys.stdin], [], [], 30)
        if i:
            dobot.verbose("OK")
            # demo onderbroken
            demo = False
        else:
            # random computer speler
            dobot.verbose("Duurt lang! Ik doe het wel voor je...")
            pallet.pak_pallet_volgende()
            ( k,r ) = random.choice(get_available_moves(board))
            return ( r,k )

    pallet.pak_pallet_volgende()

    dobot.verbose("Gebruikt pijltjes toetsen om een locatie te kiezen en druk op ENTER. (d=demo mode, q=quit)")
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
        elif key == 'd':
            dobot.verbose("Demo mode")
            demo=True
            # random computer speler
            (k,r ) = random.choice(get_available_moves(board))
            return ( r, k )
        elif key == 'q':
            sys.exit(1)

        #limiteer bereik
        r=max(-2,r)
        r=min(4,r)
        k=max(-2,k)
        k=min(4,k)

import sys, select



while True:
    board, winner = EMPTY_BOARD, None

    demo=True
    dobot.home()

    while winner is None:
        print(get_printable_board(board))

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
                dobot.error("Mag niet!")

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
    if winner == 'T' or winner=='X':
        dobot.error("A strange game. The only winning move is not to play.")
        sad()
    else:
        dobot.verbose("HA Ik heb gewonnen!")
        happy()

    sleep(5)
    dobot.verbose("Aan het opruimen...")
    pallet.opruimen()
