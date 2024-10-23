#!/usr/bin/env python3
from time import sleep

from dobotfun.dobotfun import DobotFun
import pydobot
from pydobot.dobot import Position

import config
delay=5

robot=DobotFun()

# robot.alarm_check=False
# robot.home()

# robot.move_to_pos(config.middle)

# robot.move_to_pos(config.lu)
# sleep(delay)
#
# robot.hop_to_pos(config.ru)
# sleep(delay)
#
# robot.hop_to_pos(config.rl)
# sleep(delay)
#
# robot.hop_to_pos(config.ll)
# sleep(delay)


robot.move_to(config.lu.x, config.lu.y, config.cam_z,0)
sleep(delay)
robot.move_to(config.ru.x, config.ru.y, config.cam_z,0)
sleep(delay)
robot.move_to(config.ll.x, config.ll.y, config.cam_z,0)
sleep(delay)
robot.move_to(config.rl.x, config.rl.y, config.cam_z,0)
sleep(delay)

# robot.move_to(config.lu.x, config.lu.y, config.point_z,0)
# sleep(delay)
# robot.move_to(config.ru.x, config.ru.y, config.point_z,0)
# sleep(delay)
# robot.move_to(config.ll.x, config.ll.y, config.point_z,0)
# sleep(delay)
# robot.move_to(config.rl.x, config.rl.y, config.point_z,0)
# sleep(delay)
