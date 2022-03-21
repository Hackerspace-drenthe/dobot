#GPL3.0 - (c)edwin@datux.nl
import sys
from time import sleep, time

import colorama
from serial.tools import list_ports

from .LogConsole import LogConsole
from pydobot import Dobot
from pydobot.dobot import MODE_PTP


class DobotFun(Dobot):

    #loggen (handig als je meerdere reobots hebt)
    def verbose(self, txt):
        self.log.verbose(f"{self.id}: {txt}")

    def debug(self, txt):
        self.log.debug(f"{self.id}: {txt}")

    def warning(self, txt):
        self.log.warning(f"{self.id}: {txt}")

    def error(self, txt):
        self.log.error(f"{self.id}: {txt}")


    def __init__(self, port=None, id=None):

        #(dobot class logt ook nog via logger, maar deze is handiger)
        self.log=LogConsole(show_debug=True, show_verbose=True, color=True)

        self.id=""

        if port is None:
            self.log.verbose("Gedetecteerde poorten:")
            ports=list_ports.comports()
            if ports:
                for p in ports:
                    print (" "+str(p))
            else:
                self.log.error("Geen compoorten gevonden")
                sys.exit(1)

            self.log.verbose ("")

            port = ports[0].device

        if id is None:
            self.id=port
        else:
            self.id=id

        self.verbose(f"Connectie maken naar poort {port} ")
        super().__init__(port=port)

        self.suck_delay=0.5
        self.los()
        self.sucking=False
        self.alarm_check=True


        #gevoeligheid van lost step detectie (2 is te krap)
        self.set_lost_step_params(4)
        # self.home()

    def format_pose(self):
        p=self.get_pose()
        return f"x={p.position.x:.2f}, y={p.position.y:.2f}, z={p.position.z:.2f}, r={p.position.r:.2f}"

    def show_progress(self, extra_info=""):
        pose=self.format_pose()
        self.log.progress(f"[ {pose} ] {extra_info}")


    def wacht_op(self, cmd_id):
        """wacht op command en toon mooie progress info op beeld. ook error handeling"""

        last_change=time()
        prev_pose=self.get_pose().position

        current_cmd_id = self._get_queued_cmd_current_index()
        while cmd_id > current_cmd_id:
            self.show_progress(colorama.Back.RED + f"Bezig... " + colorama.Style.RESET_ALL)
            current_cmd_id = self._get_queued_cmd_current_index()

            #alarm?
            if self.alarm_check:
                alarms = self.get_alarms()
                if alarms:
                    self.error(f"Alarm: {', '.join(map(str, alarms))}.")
                    sys.exit(1)

            #still moving?
            p=self.get_pose().position
            if (p.x!=prev_pose.x or p.y!=prev_pose.y or p.z!=prev_pose.z or p.r!=prev_pose.r):
                last_change=time()
                prev_pose=p

            #te lang niet verplaatst? dit gebeurd door de lost step detectie, robot komt dan niet op zn doel plaats.
            if time()-last_change>5:

                self.error(f"Timeout! (ergens tegenaan gekomen?) ")
                sys.exit(1)
                return



        self.show_progress(colorama.Back.GREEN + "Klaar"+colorama.Style.RESET_ALL)

    def vast(self):
        self.sucking=True
        self.wacht_op(self.suck(True))
        # sleep(self.suck_delay)

    def los(self):
        self.sucking=False
        self.wacht_op(self.suck(False))
        sleep(self.suck_delay)

    def home(self):
        self.verbose("Thuis positie opzoeken...")
        self.wacht_op(super().home())

    def move_to(self, x, y, z, r=0., mode=None):
        self.debug(f"move_to x={x:.2f}, y={y:.2f}, z={z:.2f}, r={r:.2f}")
        #deze zorgt dat een command pas ready is als hij op de plaats van bestemming is (ongeveer)
        self.set_lost_step_command()
        id = super().move_to(x, y, z, r, MODE_PTP.MOVJ_XYZ)
        self.wacht_op(id)
        return id

    def move_to_pos(self, p):
        self.move_to(p.x, p.y, p.z, p.r)

    def hop_to(self, x, y, z, r=0.):
        self.debug(f"hop_to x={x}, y={y}, z={z}, r={r}")
        id = super().move_to(x, y, z, r, MODE_PTP.JUMP_MOVL_XYZ)
        self.wacht_op(id)
        return id

    def hop_to_pos(self, pos):
        self.hop_to(pos.x, pos.y, pos.z, pos.r)
        return id


    def move_to_nowait(self, x, y, z, r=0., mode=MODE_PTP.MOVJ_XYZ):
        self.debug(f"move_to x={x}, y={y}, z={z}, r={r}")
        id=super().move_to(x, y, z, r, mode)
        self.show_progress()
        return id

    def __del__(self):
        pass
        # if self.id:
        #     try:
        #         self.verbose(f"Connectie naar robot {self.id} gesloten")
        #         self.los()
        #     except:
        #         pass


    def get_pos(self):
        return self.get_pose().position


    def snel(self):
        self.speed(100,100)

    def langzaam(self):
        self.speed(5,5)
