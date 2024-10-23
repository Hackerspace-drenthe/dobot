from pydobot.dobot import Position

#vanaf hoe hoog kijkt de cam
cam_z=100

point_z=-22

middle=Position(227+30,0,cam_z,0)


# x++ = naar voren
# y++ = naar links
x_offset=50
y_offset=100

# links rechts boven onder calibratie posities

lu=Position(middle.x+x_offset,middle.y+y_offset,point_z,0)
ru=Position(middle.x+x_offset,middle.y-y_offset,point_z,0)

ll=Position(middle.x-x_offset,middle.y+y_offset,point_z,0)
rl=Position(middle.x-x_offset,middle.y-y_offset,point_z,0)
