#!/usr/bin/env python3

from dobotfun.dobotfun import DobotFun

robot=DobotFun()

p=robot.get_pos()
p.z=p.z+50
robot.alarm_check=False
robot.move_to_pos(p)
robot.home()
