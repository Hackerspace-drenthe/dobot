#!/usr/bin/env python
from dobotfun.dobotfun import DobotFun
from pydobot.dobot import Position
from pydobot.keyboardcontrol import KeyboardControl
import pickle

from pydobot.palletfun import PalletFun

dobot=DobotFun()

pallet=PalletFun(dobot)

# for r in range (0,3):
#     for k in range(0,3):
#         pallet.pak_pallet_volgende()
#         pallet.zet(200 + (27*r),0+(27*k))

s=25
h=s/2

pallet.pak_pallet_volgende()
pallet.zet(150,-s)
pallet.pak_pallet_volgende()
pallet.zet(150,0)
pallet.pak_pallet_volgende()
pallet.zet(150,s)

pallet.pak_pallet_volgende()
pallet.zet(150,+h,1 )
pallet.pak_pallet_volgende()
pallet.zet(150,-h,1)

pallet.pak_pallet_volgende()
pallet.zet(150,0,2)

pallet.opruimen()
