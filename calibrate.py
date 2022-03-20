#!/usr/bin/env python
from time import sleep

from dobotfun.dobotfun import DobotFun
from dobotfun.keyboardcontrol import KeyboardControl
from pydobot.dobot import MODE_PTP

d=DobotFun(None, "Dobot")

#d.set_angle_sensor_static_error(0,0)
# d.home()

(rear, front) = d.get_angle_sensor_static_error()
d.warning(f"Static error: {rear:5f} {front:5f}")
sys.exit(1)
z=-68
z=0
d._set_ptp_cmd(210,-40,z,0,MODE_PTP.MOVJ_XYZ)
sleep(1)
d._set_ptp_cmd(210,40,z,0,MODE_PTP.MOVJ_XYZ)

#k=KeyboardControl(d)
#k.get()
