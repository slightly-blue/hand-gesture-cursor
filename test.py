from touch_emulation import make_touch, move_cursor, pointer_click, initiate_touch, release_touch, drag_touch, drag_emulation

from touch_manager import TouchManager
# Click on windows logo on primary screen 

#make_touch(x=20, y=1060, fingerRadius=4)

# initiate_touch(x=100, y=100)
# drag_touch(x=550, y=1200)
# release_touch(x=980, y=1820)

#release_touch(x=100, y=100)

#move_cursor(x=20, y=1060)

#pointer_click(x=20, y=1060)



manager = TouchManager(x=300, y=300)
# manager.drag_update(x=200, y=200)
# manager.drag_update(x=300, y=300)
# manager.drag_update(x=400, y=400)
# manager.drag_update(x=500, y=500)
# manager.release_touch(x=500, y=500)


for val in range(500):
    manager.drag_update(x=300 + val, y=300)

manager.release_touch()

#drag_emulation(x1=200, y1=200)

# TODO
# Figure out why a drag action can not be staged 