
#GPL3.0 - (c)edwin@datux.nl
import pickle
import sys
import os
import logging

from pydobot.dobot import Position


class PalletConfig:
    """berekening en configuratie van Pallet. een 4x4 grid van blokjes. gebruikt pallet_leer.py om te calibreren"""

    def __init__(self):
        self.grid_size=4
        self.z=-47
        self.lb=Position()
        self.rb=Position()
        self.lo=Position()
        self.ro=Position()

    def print(self):
        print ("")
        print (f"Pallet config {self.grid_size} x {self.grid_size}:")
        print(f" 1 LB: x{self.lb.x:.2f} y{self.lb.y:<2.2f}\t2 RB: x{self.rb.x:.2f} y{self.rb.y:.2f}")
        print(f" 3 LO: x{self.lo.x:.2f} y{self.lo.y:<2.2f}\t4 RO: x{self.ro.x:.2f} y{self.ro.y:.2f}")
        print(f"Z hoogte: {self.z:.2f}")

    def pos(self, r, k):
        """bepaal positie, returned x,y"""
        x_factor = (r - 1) / (self.grid_size - 1)
        y_factor = (k - 1) / (self.grid_size - 1)

            # links boven                                 rechts boven                            #  links onder                          # rechts onder
        x = self.lb.x * (1 - x_factor) * (1 - y_factor) + self.rb.x * (1 - x_factor) * y_factor + self.lo.x * x_factor * (1 - y_factor) + self.ro.x * x_factor * y_factor
        y = self.lb.y * (1 - x_factor) * (1 - y_factor) + self.rb.y * (1 - x_factor) * y_factor + self.lo.y * x_factor * (1 - y_factor) + self.ro.y * x_factor * y_factor

        return x, y

    @staticmethod
    def load():
        if os.path.exists("pallet.config"):
            with open('pallet.config','rb') as f:
                return pickle.load(f)
        else:
            return PalletConfig()

    def save(self):
        with open('pallet.config','wb') as f:
            pickle.dump(self,f)
        print ("config saved")


class PalletFun():
    def __init__(self, dobot):

        self.p=PalletConfig.load()
        self.p.print()

        self.d=dobot


        self.pallet_aanwezig = [
            (1, 1),
            (1, 2),
            (2, 1),
            (1, 3),
            (2, 2),
            (3, 1),
            (1, 4),
            (2, 3),
            (3, 2),
            (4, 1),
            (2, 4),
            (3, 3),
            (4, 2),
            (3, 4),
            (4, 3),
            (4, 4)
        ]

        self.pallet_in_gebruik = []

        self.locaties = []

    def pak_pallet(self, r, k):
        (x, y) = self.p.pos(r, k)
        self.d.hop_to(x,y,self.p.z)
        self.d.vast()
        self.d.langzaam()
        self.d.move_to(x+5,y+5,self.p.z-5)




    def zet_pallet(r, k):
        (x, y) = calc_pallet(r, k)
        device.move_to(x + 5, y + 5, grond_z + 50)
        device.move_to(x + 5, y + 5, grond_z)
        device.speed(10, 10)
        device.move_to(x, y, grond_z)
        device.wait_for_cmd(device.suck(False))
        device.wait_for_cmd(device.move_to(x - 1, y - 1, grond_z))
        device.speed(100, 100)
        sleep(suck_delay)
        device.wait_for_cmd(device.move_to(x, y, grond_z + 50))


    def zet(x, y, z):
        device.move_to(x, y, z + 30)
        device.move_to(x, y, z)
        device.wait_for_cmd(device.suck(False))
        sleep(suck_delay)
        device.speed(10, 10)
        device.move_to(x, y, z + 30)
        device.speed(100, 100)
        locaties.insert(0, (x, y, z))


    def cleanup():
        for locatie in locaties:
            pak(locatie[0], locatie[1], locatie[2])
            zet_pallet_volgende()
        locaties.clear()


    def pak(x, y, z):
        device.move_to(x, y, z + 30)
        device.move_to(x, y, z)
        device.wait_for_cmd(device.suck(True))
        sleep(suck_delay)
        device.move_to(x, y, z + 30)


    def pak_pallet_volgende():
        (r, k) = pallet_aanwezig.pop(0)
        pallet_in_gebruik.insert(0, (r, k))
        pak_pallet(r, k)


    def zet_pallet_volgende():
        (r, k) = pallet_in_gebruik.pop(0)
        pallet_aanwezig.insert(0, (r, k))
        zet_pallet(r, k)


# print("Pallet coords:")
# for r in reversed(range(1, 5)):
#     for k in reversed(range(1, 5)):
#         (x, y) = calc_pallet(r, k)
#         print(f"{x:.1f},{y:.1f}\t", end='')
#         # print(f"{r},{k}\t", end='')
#     print()
#
# logging.Logger("Dobot", logging.DEBUG)
#
# port = list_ports.comports()[0].device
# device = Dobot(port=port)
#
# for nr in range(0, 3):
#     pak_pallet_volgende()
#     zet(240 - int(nr / 8) * 40, (nr % 8) * 40 + (-120), grond_z)
#
# locaties.reverse()
#
# cleanup()
