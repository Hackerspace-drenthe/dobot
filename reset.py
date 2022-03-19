import logging

import dobotfun

robot=dobotfun.DobotFun()
#
# print ("Robot word gehomed")

# robot.home()
# robot.move()

robot.move_to(2,100,16)
robot.move_to(2,200,16)



# while True:
    # print (robot._get_queued_cmd_current_index())
    # print(robot.get_pose())