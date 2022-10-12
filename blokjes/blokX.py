import cadquery as cq
from cadquery import exporters

# Make a cube of 25 mm with the letter X on all sides

height = 25
width = 25
thickness = 25

# Make the cube
result = (cq.Workplane("XY")
        .box(height, width, thickness)
        # Project the X on the topside
        .faces(">Z").workplane()
        .text("X", 20, -0.2)
        # Project the O on the bottomside
        .faces("<Z").workplane()
        .text("O", 20, -0.2)
        )

show_object(result)
exporters.export(result, './block.amf')
