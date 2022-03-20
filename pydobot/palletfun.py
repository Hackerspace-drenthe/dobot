# GPL3.0 - (c)edwin@datux.nl
import pickle
import sys
import os
import logging

from pydobot.dobot import Position


class PalletConfig:
    """berekening en configuratie van Pallet. een 4x4 grid van blokjes. gebruikt pallet_leer.py om te calibreren"""

    def __init__(self):
        self.grid_size = 4
        self.z = -47
        self.lb = Position()
        self.rb = Position()
        self.lo = Position()
        self.ro = Position()

    def print(self):
        print("")
        print(f"Pallet config {self.grid_size} x {self.grid_size}:")
        print(f" 1 LB: x{self.lb.x:.2f} y{self.lb.y:<2.2f}\t2 RB: x{self.rb.x:.2f} y{self.rb.y:.2f}")
        print(f" 3 LO: x{self.lo.x:.2f} y{self.lo.y:<2.2f}\t4 RO: x{self.ro.x:.2f} y{self.ro.y:.2f}")
        print(f"Z hoogte: {self.z:.2f}")

    def pos(self, r, k):
        """bepaal positie, returned x,y"""
        x_factor = (r - 1) / (self.grid_size - 1)
        y_factor = (k - 1) / (self.grid_size - 1)

        # links boven                                 rechts boven                            #  links onder                          # rechts onder
        x = self.lb.x * (1 - x_factor) * (1 - y_factor) + self.rb.x * (
                1 - x_factor) * y_factor + self.lo.x * x_factor * (1 - y_factor) + self.ro.x * x_factor * y_factor
        y = self.lb.y * (1 - x_factor) * (1 - y_factor) + self.rb.y * (
                1 - x_factor) * y_factor + self.lo.y * x_factor * (1 - y_factor) + self.ro.y * x_factor * y_factor

        return x, y

    @staticmethod
    def load():
        if os.path.exists("pallet.config"):
            with open('pallet.config', 'rb') as f:
                return pickle.load(f)
        else:
            return PalletConfig()

    def save(self):
        with open('pallet.config', 'wb') as f:
            pickle.dump(self, f)
        print("config saved")


class PalletFun():
    def __init__(self, dobot):
        self.p = PalletConfig.load()
        self.p.print()

        self.d = dobot

        self.block_size = 25

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

        self.pak_marge = 6

    def pak_pallet(self, r, k):
        """pak iets heel voorzichtig van pallet"""
        (x, y) = self.p.pos(r, k)
        self.d.move_to(x, y, self.p.z + self.pak_marge + self.block_size)
        self.d.move_to(x, y, self.p.z )
        self.d.vast()
        # self.d.langzaam()
        # self.d.move_to(x, y , self.p.z + self.pak_marge)
        # self.d.snel()
        self.d.move_to(x + self.pak_marge, y + self.pak_marge, self.p.z + self.pak_marge + self.block_size)

    def zet_pallet(self, r, k):
        (x, y) = self.p.pos(r, k)

        #zorg dat we hoog genoeg blijven
        pos=self.d.get_pos()

        self.d.move_to(x + self.pak_marge, y + self.pak_marge, pos.z)
        self.d.move_to(x + self.pak_marge, y + self.pak_marge, self.p.z+ self.pak_marge)
        self.d.langzaam()
        self.d.move_to(x, y, self.p.z + self.pak_marge)
        self.d.move_to(x, y, self.p.z )
        self.d.los()
        self.d.move_to(x - 2, y - 2, self.p.z)
        self.d.move_to(x - 2, y - 2, self.p.z + self.pak_marge)
        self.d.snel()

    def pak_pallet_volgende(self):
        """pak eerst volgende blokje van pallet"""
        (r, k) = self.pallet_aanwezig.pop(0)
        self.pallet_in_gebruik.insert(0, (r, k))
        self.pak_pallet(r, k)

    def zet_pallet_volgende(self):
        """zet blokjes op eerst volgende vrije plek op pallet"""
        (r, k) = self.pallet_in_gebruik.pop(0)
        self.pallet_aanwezig.insert(0, (r, k))
        self.zet_pallet(r, k)

    def zet(self, x, y, laag=0):
        """zet neer op een plek en onthou positie voor cleanup"""

        z=self.p.z + self.block_size*laag

        #zorg dat we hoog genoeg zitten voor we wat doen
        pos=self.d.get_pos()
        pos.z=z+self.pak_marge+self.block_size
        self.d.move_to_pos(pos)

        self.d.move_to(x, y, z+self.pak_marge+self.block_size)
        # self.d.move_to(x, y, z+self.pak_marge)
        # self.d.langzaam()
        self.d.move_to(x, y, z)
        self.d.los()
        self.d.move_to(x, y, z+self.pak_marge)
        # self.d.snel()
        self.locaties.insert(0, (x, y, laag))

    def pak(self,x, y, laag=0):
        z=self.p.z + self.block_size*laag

        #zorg dat we hoog genoeg zitten voor we wat doen
        pos=self.d.get_pos()
        pos.z=z+self.pak_marge
        self.d.move_to_pos(pos)

        self.d.move_to(x, y, z+self.pak_marge)
        # self.d.langzaam()
        self.d.move_to(x, y, z)
        self.d.vast()
        # self.d.move_to(x, y, z+self.pak_marge)
        # self.d.snel()
        self.d.move_to(x, y, z+self.pak_marge+self.block_size)



    def opruimen(self):
        for locatie in self.locaties:
            ( x,y,laag )=locatie
            self.pak(x,y,laag)
            self.zet_pallet_volgende()
        self.locaties.clear()


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
