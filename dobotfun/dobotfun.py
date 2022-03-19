#GPL3.0 - (c)edwin@datux.nl
import sys

from serial.tools import list_ports

from .LogConsole import LogConsole
from pydobot import Dobot
from pydobot.dobot import MODE_PTP


class DobotFun(Dobot):

    #loggen (handig als je meerdere reobots hebt)
    def verbose(self, txt):
        self.log.verbose(f"{self.id: <16}: {txt}")

    def debug(self, txt):
        self.log.debug(f"{self.id: <16}: {txt}")

    def warning(self, txt):
        self.log.warning(f"{self.id: <16}: {txt}")

    def error(self, txt):
        self.log.error(f"{self.id: <16}: {txt}")


    def __init__(self, port=None, id=None):

        #(dobot class logt ook nog via logger, maar deze is handiger)
        self.log=LogConsole(show_debug=True, show_verbose=True, color=True)

        if port is None:
            self.log.verbose("Gedetecteerde poorten:")
            for p in list_ports.comports():
                print (" "+str(p))

            self.log.verbose ("")
            port = list_ports.comports()[0].device

        if id is None:
            self.id=port
        else:
            self.id=id

        self.verbose(f"Connectie maken naar poort {port} ")
        super().__init__(port=port)

        self.suck(False)

    def format_pose(self):
        p=self.get_pose()
        return f"x={p.position.x:.2f}, y={p.position.y:.2f}, z={p.position.z:.2f}, r={p.position.r:.2f}"

    def show_progress(self, extra_info=""):
        pose=self.format_pose()
        self.log.progress(f"[ {pose} ] {extra_info}")


    def wacht_op(self, cmd_id, check_alarm=True):
        """wacht op command en toon mooie progress info op beeld. ook error handeling"""

        current_cmd_id = self._get_queued_cmd_current_index()
        while cmd_id > current_cmd_id:
            self.show_progress(f"Commando {current_cmd_id}/{cmd_id}")
            current_cmd_id = self._get_queued_cmd_current_index()

            #alarm?
            if check_alarm:
                alarms = self.get_alarms()
                if alarms:
                    self.error(f"Alarm: {', '.join(map(str, alarms))}.")
                    sys.exit(1)

        self.show_progress("Klaar")

    def home(self):
        self.verbose("Thuis positie opzoeken...")
        self.wacht_op(super().home())

    def move_to(self, x, y, z, r=0., mode=MODE_PTP.MOVJ_XYZ):
        self.debug(f"move_to x={x}, y={y}, z={z}, r={r}")
        id = super().move_to(x, y, z, r, mode)
        self.wacht_op(id)
        return id

    def move_to_nowait(self, x, y, z, r=0., mode=MODE_PTP.MOVJ_XYZ):
        self.debug(f"move_to x={x}, y={y}, z={z}, r={r}")
        id=super().move_to(x, y, z, r, mode)
        self.show_progress()
        return id

    def __del__(self):
        self.verbose(f"Connectie naar robot {self.id} gesloten")
