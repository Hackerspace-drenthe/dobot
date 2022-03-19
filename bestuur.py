import sys

from dobotfun.dobotfun import DobotFun
from pydobot.keyboardcontrol import KeyboardControl


d=DobotFun()

k=KeyboardControl(d)

k.get()


