#!/usr/bin/env python3
import sys

from dobotfun.dobotfun import DobotFun
from dobotfun.keyboardcontrol import KeyboardControl

d=DobotFun(None, "Dobot")

k=KeyboardControl(d)
k.get()


