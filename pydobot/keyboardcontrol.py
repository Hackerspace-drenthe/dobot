#(C)2022 edwin@datux.nl
import sys
import termios

from pynput import keyboard


class KeyboardControl:

    def __init__(self, dobot):

        self.d = dobot
        self.d.log.show_debug = False
        self.d.alarm_check=False

    def get(self):
        """lets user control until enter or esc is pressed. when enter is pressed the selected position is returned"""

        print(
            """
Besturing:
 * x en y coordinaten: Pijltjes toetsen
 * Hoogtee           : PgUp/PgDn
 * Draaien           : , en .
 * Snelheid          : getal 1 t/m 5
 * Calibreren        : h 
 * Ga naar thuis     : r
 * Sla thuis op      : s
 * Stoppen           : ESC
 * Opslaan           : ENTER
"""
        )

        self.p = self.d.get_pose().position

        self.step_size = 1

        self.result = None
        self.changed = True

        def on_press(key):
            self.changed = True

            # print('special key pressed: {0}'.format(key))
            if key == keyboard.Key.enter:
                self.result = self.p
                return False
            elif key == keyboard.Key.esc:
                self.result = False
                return False
            elif key == keyboard.Key.up:
                self.p.x = self.p.x + self.step_size
            elif key == keyboard.Key.down:
                self.p.x = self.p.x - self.step_size
            elif key == keyboard.Key.left:
                self.p.y = self.p.y + self.step_size
            elif key == keyboard.Key.right:
                self.p.y = self.p.y - self.step_size
            elif key == keyboard.Key.page_up:
                self.p.z = self.p.z + self.step_size
            elif key == keyboard.Key.page_down:
                self.p.z = self.p.z - self.step_size
            elif hasattr(key, 'char'):
                if key.char == 'r':
                    self.d.verbose("Reset position")
                    #note: zelfde positie als plek waar hij homed. scheelt tijd
                    self.p.x = 0
                    self.p.y = -100
                    self.p.z = 0
                    self.p.r = 0
                elif key.char == 'h':
                    self.d.home()
                elif key.char == 's':
                    self.d.verbose("Nieuwe thuispositie opgeslagen")
                    self.d.set_home(self.p.x, self.p.y, self.p.z)
                elif key.char == ',':
                    self.p.r = self.p.r - self.step_size
                elif key.char == '.':
                    self.p.r = self.p.r + self.step_size
                elif key.char == '1':
                    self.step_size = 0.1
                    self.d.verbose(f"Speed = {self.step_size}mm")
                elif key.char == '2':
                    self.step_size = 0.5
                    self.d.verbose(f"Speed = {self.step_size}mm")
                elif key.char == '3':
                    self.step_size = 1
                    self.d.verbose(f"Speed = {self.step_size}mm")
                elif key.char == '4':
                    self.step_size = 5
                    self.d.verbose(f"Speed = {self.step_size}mm")
                elif key.char == '5':
                    self.step_size = 10
                    self.d.verbose(f"Speed = {self.step_size}mm")
                elif key.char == '6':
                    self.step_size = 25
                    self.d.verbose(f"Speed = {self.step_size}mm")

        def on_release(key):
            # print('special key released: {0}'.format(
            #     key))
            self.changed = True
            pass

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:

            while self.result is None:
                # ( cx, cy, cz, cr)=d.get_pose().position

                # if cx!=x or cy!=y or cz!=z or cr!=r:
                if self.changed:
                    self.changed = False
                    self.d.move_to_pos(self.p)

                    if self.d.get_alarms():
                        # try to recover
                        self.d.clear_alarms()
                        self.d.move_to_pos(self.p)
                        if self.d.get_alarms():
                            self.d.error("Alarm, ga terug of druk op 'r'")
            listener.join()
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

        return (self.result)