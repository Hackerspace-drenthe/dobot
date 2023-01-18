#!/usr/bin/env python3
import signal
import sys
from time import sleep

from dobotfun.dobotfun import DobotFun

from dobotfun.palletfun import PalletFun
from tictactoe import *
import os
# def interrupted(signum, frame):
#     "called when read times out"
#     print ('interrupted!')
#
# signal.signal(signal.SIGALRM, interrupted)
# signal.alarm(3)
#
# play_console_game()

import readchar

dobot = DobotFun(port=None, id="WOPR")
dobot.log.show_debug=True
pallet = PalletFun(dobot, grid_size=3)

block_size = 29
x_start = 210
y_start = -45
optil_z = pallet.pallet_config.z + block_size + 10


def calc_grid_positie(r, k):
    return (x_start + (r * block_size), y_start + (k * block_size))
    #hack voor mijn afwijkende dobot
    #return (x_start + (r * block_size), y_start + k*block_size*0.8)

def sad():
    # :( verloren
    x=x_start
    dobot.speed(5,100)
    dobot.move_to(x_start, -150, pallet.pallet_config.z)
    dobot.speed(5,1)
    dobot.move_to(x_start, -150, pallet.pallet_config.z-10)
    dobot.snel()

def happy():
    x=x_start

    # :)  gewonnne \o/
    dobot.move_to(x, 0, 160)
    dobot.move_to(x, 0, 160)
    dobot.move_to(x, 0, 140)
    dobot.move_to(x, 0, 160)
    dobot.move_to(x, 0, 140)
    dobot.move_to(x, 0, 160)
    dobot.move_to(x, 0, 140)
    dobot.snel()

# happy()
# sad()
# sys.exit(1)

def move_for_player():
    """make move for player, but first move is random"""
    moves = get_available_moves(board)
    if len(moves) == 9:
        (k, r) = random.choice(moves)
    else:
        (k, r) = minimax(board, 'X')

    return (k, r)


demo=True

def bestuur_positie( r,k ):
    """laat de player een positie kiezen met pijltjes"""


    global demo
    if demo:
        os.system('clear')
        print()
        print()
        print()
        print()
        dobot.verbose("SHALL WE PLAY A GAME?")
        i, o, e = select.select([sys.stdin], [], [], 15)
        if i:
            dobot.verbose("FINE")
            # demo onderbroken
            demo = False
        else:
            #timeout, let computer make move for player
            dobot.verbose("TIMEOUT")
            pallet.pak_pallet_volgende()
            (k,r)=move_for_player()
            return ( r,k )

    pallet.pak_pallet_volgende()

    # dobot.verbose("Gebruikt pijltjes toetsen om een locatie te kiezen en druk op ENTER. ")
    # dobot.verbose("(d=demo mode, q=stoppen, h=herstarten")
    dobot.verbose("PLEASE CHOOSE A LOCATION.")
    while True:
        (x,y)=calc_grid_positie( r, k )
        dobot.move_to_nowait( x,y, optil_z )

        key = readchar.readkey()
        if key == readchar.key.ENTER:
            dobot.verbose("FINE")
            return ( r,k )
        elif key == "9":
            k = 2
            r = 0
        elif key == "8":
            k = 1
            r = 0
        elif key == "7":
            k = 0
            r = 0
        elif key == "6":
            k = 2
            r = 1
        elif key == "5":
            k = 1
            r = 1
        elif key == "4":
            k = 0
            r = 1
        elif key == "3":
            k = 2
            r = 2
        elif key == "2":
            k = 1
            r = 2
        elif key == "1":
            k = 0
            r = 2
        elif key == readchar.key.RIGHT:
            k = k + 1
        elif key == readchar.key.LEFT:
            k = k - 1
        elif key == readchar.key.UP:
            r = r - 1
        elif key == readchar.key.DOWN:
            r = r + 1
        elif key == 'd' or key=='*':
            dobot.verbose("Demo mode")
            demo=True
            # play against self, but first move is random
            (k,r)=move_for_player()
            return ( r, k )
        elif key == 'q':
            dobot.los()
            sys.exit(1)
        elif key == 'h':
            return None

        #limiteer bereik
        r=max(-2,r)
        r=min(4,r)
        k=max(-2,k)
        k=min(4,k)

import sys, select



while True:
    board, winner = EMPTY_BOARD, None

    demo=True
    herstart=False
    #dobot.home()

    while winner is None and not herstart:
        print(get_printable_board(board))

        r=0
        k=0
        while not herstart:
            try:
                p=bestuur_positie(r,k)
                if p is None:
                    herstart=True
                    break
                (r,k) = p

                board, winner = play(board, 'X', k, r)

                #gelukt, plaats blokje
                ( x,y )= calc_grid_positie(r,k)
                pallet.zet(x,y)

                break
            except (IllegalMove, ValueError):
                # dobot.error("Mag niet!")
                dobot.error("ILLEGAL MOVE!")

                #ongeldige move, schud nee
                ( x,y )= calc_grid_positie(r,k)
                dobot.move_to(x,y+3, optil_z)
                dobot.move_to(x,y, optil_z)
                dobot.move_to(x,y+3, optil_z)

            except KeyboardInterrupt:
                exit()

        if winner is None:
            dobot.verbose("MY MOVE..")
            pallet.pak_pallet_volgende()
            moves = get_available_moves(board)
            if (random.random()<0.2):
               (k, r) = random.choice(moves)
            else:
               (k, r) = minimax(board, 'O')
            (x, y) = calc_grid_positie(r, k)
            pallet.zet(x, y)
            board, winner = play(board, 'O', k, r)

    print(get_printable_board(board))
    if winner == 'T' or winner=='X':
        dobot.error("A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.")
        sad()
    else:
        dobot.verbose("I WON")
        happy()

    sleep(2)
    dobot.verbose("LETS PLAY AGAIN")
    pallet.opruimen()
