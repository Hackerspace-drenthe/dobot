#!/usr/bin/env python
from dobotfun.dobotfun import DobotFun
from pydobot.dobot import Position
from pydobot.keyboardcontrol import KeyboardControl
import pickle

from pydobot.palletfun import PalletFun

dobot=DobotFun()

pallet=PalletFun(dobot)


pallet.pak_pallet_volgende()
pallet.zet(200,0)

pallet.pak_pallet_volgende()
pallet.zet(200,30)
pallet.opruimen()
