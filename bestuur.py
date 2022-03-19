from pynput import keyboard

from dobotfun.dobotfun import DobotFun

d=DobotFun()
d.log.show_debug=False

( x,y,z,r ) = d.get_pose().position
changed=False

x=int(x)
y=int(y)
z=int(z)
r=int(r)

step_size=10


def on_press(key):
    global x,y,z,r, changed, step_size

    changed=True
    # print('special key pressed: {0}'.format(key))



    if key==keyboard.Key.up:
        x=x+step_size
    elif key==keyboard.Key.down:
        x=x-step_size
    elif key==keyboard.Key.left:
        y=y+step_size
    elif key==keyboard.Key.right:
        y=y-step_size
    elif key==keyboard.Key.page_up:
        z=z+step_size
    elif key==keyboard.Key.page_down:
        z=z-step_size
    elif hasattr(key, 'char'):
        if key.char=='r':
            d.verbose("Reset position")
            x=150
            y=0
            z=0
            r=0
        elif key.char == ',':
            r = r - step_size
        elif key.char == '.':
            r = r + step_size
        elif key.char=='1':
            step_size=0.1
            d.verbose(f"Speed = {step_size}mm")
        elif key.char=='2':
            step_size=0.5
            d.verbose(f"Speed = {step_size}mm")
        elif key.char=='3':
            step_size=1
            d.verbose(f"Speed = {step_size}mm")
        elif key.char=='4':
            step_size=5
            d.verbose(f"Speed = {step_size}mm")
        elif key.char=='5':
            step_size=10
            d.verbose(f"Speed = {step_size}mm")




def on_release(key):
    # print('special key released: {0}'.format(
    #     key))
    pass


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:

    while True:
        # ( cx, cy, cz, cr)=d.get_pose().position

        # if cx!=x or cy!=y or cz!=z or cr!=r:
        if changed:
            changed=False
            id=d.move_to_nowait(x,y,z,r)
            d.wacht_op(id, check_alarm=False)

            if d.get_alarms():
                #try to recover
                d.clear_alarms()
                id=d.move_to_nowait(x,y,z,r)
                d.wacht_op(id, check_alarm=False)
                if d.get_alarms():
                    d.error("Alarm.")




    # listener.join()

