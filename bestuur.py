#!/usr/bin/env python

from dobotfun.dobotfun import DobotFun
from dobotfun.keyboardcontrol import KeyboardControl

d=DobotFun(None, "Dobot")

k=KeyboardControl(d)
k.get()


