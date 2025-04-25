# %%

import cadquery as cq
import const as c
import ocp_vscode as ov
import util as u

battery_mount = (
    cq.Workplane("XY")
    .rect(7 + 2 * c.wall_thickness, c.shield_width)
    .rect(7 + 2 * c.wall_thickness + 8, 20)
    .extrude(1)
    .faces(">Z")
    .rect(7 + c.wall_thickness, c.shield_width - 5, forConstruction=True)
    .vertices()
    .rect(c.wall_thickness, 5)
    .extrude(5)
    .faces(">X[1]")
    .workplane(centerOption="CenterOfMass")
    .move(xDist=-0.5 * c.shield_width + 2.5)
    .hLine(c.shield_width - 5, forConstruction=True)
    .vertices()
    .circle(1.6)
    .cutThruAll()
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .move(xDist=-7)
    .hLine(14, forConstruction=True)
    .vertices()
    .circle(1.6)
    .cutThruAll()
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .rect(7, c.shield_width)
    .cutThruAll()
)

dual_battery = u.get_dual_battery().translate(
    (0, 0, c.shield_board_height * 0.5 + 1)
)

ov.show(battery_mount, dual_battery, colors=["darkgreen"])

# %%

battery_mount.export("print_files/battery_mount.stl")

# %%

battery_spacer = (
    cq.Workplane("XY")
    .rect(c.shield_width, 5)
    .extrude(0.6)
    .faces(">Z")
    .workplane()
    .move(xDist=-0.5 * c.shield_width + 2.5)
    .hLine(c.shield_width - 5, forConstruction=True)
    .vertices()
    .circle(1.6)
    .cutThruAll()
)

ov.show(battery_spacer)

# %%

battery_spacer.export("print_files/battery_spacer.stl")
# %%
