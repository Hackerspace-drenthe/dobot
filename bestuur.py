#!/usr/bin/env python

from dobotfun.dobotfun import DobotFun
from pydobot.keyboardcontrol import KeyboardControl

d=DobotFun()

k=KeyboardControl(d)
k.get()


