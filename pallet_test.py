#!/usr/bin/env python
from dobotfun.dobotfun import DobotFun

from dobotfun.palletfun import PalletFun

dobot = DobotFun()

pallet = PalletFun(dobot)


for y in range(-100,100,25):

    pallet.pak_pallet_volgende()
    pallet.zet(200, y)

pallet.opruimen()