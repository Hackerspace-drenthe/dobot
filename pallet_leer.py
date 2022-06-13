#!/usr/bin/env python3
from dobotfun.dobotfun import DobotFun
from dobotfun.keyboardcontrol import KeyboardControl

from dobotfun.palletfun import PalletConfig

config=PalletConfig.load(grid_size=3)

dobot=DobotFun()
keyboard_control=KeyboardControl(dobot)


while True:
    config.print()

    print()
    print("Hoofd menu:")
    print("  1 t/m  4   : Ga naar cooridnaat (en calibreer)")
    # print(" g1 t/m g4   : Ga naar coordinaat")
    print("  z          : Calibreer Z hoogte")
    # print(" gz          : Ga naar Z hoogte")
    print(" <r>,<k>     : Ga naar pallet rij, kolom (om te testen of het werkt)")
    print(" h           : Zoek thuispostitie")
    i=input("> ")

    dobot.clear_alarms()

    if i=='1':
        print ("Calibreer links boven")
        dobot.hop_to_pos(config.lb)
        p=keyboard_control.get()
        if p:
            config.lb=p
            config.save()

    if i=='2':
        print ("Calibreer rechts boven")
        dobot.hop_to_pos(config.rb)
        p=keyboard_control.get()
        if p:
            config.rb=p
            config.save()

    if i=='3':
        print ("Calibreer links onder")
        dobot.hop_to_pos(config.lo)
        p=keyboard_control.get()
        if p:
            config.lo=p
            config.save()

    if i=='4':
        print ("Calibreer rechts onder")
        dobot.hop_to_pos(config.ro)
        p=keyboard_control.get()
        if p:
            config.ro=p
            config.save()

    if i=='z':
        print ("Calibreer z hoogte")
        pose=dobot.get_pose().position
        pose.z=config.z
        dobot.hop_to_pos(pose)
        p=keyboard_control.get()
        if p:
            config.z=p.z
            config.save()

    if i=='h':
        dobot.home()

    if i[0]=='g' and len(i)==2:
        if i[1]=='1':
            dobot.hop_to_pos(config.lb)
        if i[1]=='2':
            dobot.hop_to_pos(config.rb)
        if i[1]=='3':
            dobot.hop_to_pos(config.lo)
        if i[1]=='4':
            dobot.hop_to_pos(config.ro)
        if i[1]=='z':
            p=dobot.get_pos()
            p.z=config.z
            dobot.hop_to_pos(p)

    if len(i)==3:
        r=int(i[0])
        k=int(i[2])
        (x,y)=config.pos(r,k)
        dobot.hop_to(x,y,config.z,0)


# pickle.dumps(config)
#
#
#
# print ("Huidige posities pallet:")
# # print (f" 1 (links boven) {}")
