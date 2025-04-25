# %%

import cadquery as cq
import const as c
import ocp_vscode as ov
import util as u

battery_in_case = u.get_battery_in_case().translate(
    (1, 0, c.shield_board_height * 0.5 + c.wall_thickness)
)

ov.show(battery_in_case)

# %%

battery_mount_inner_diameter = c.staff_middle_diameter - 2 * c.wall_thickness
teensy_thickness = 18
teensy_height = 35.6

wall_length = battery_mount_inner_diameter * 0.5 - 4

battery_mount = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=battery_mount_inner_diameter,
    )
    .extrude(c.wall_thickness)
    .faces(">Z")
    .tag("top")
    .workplane()
    .move(yDist=teensy_thickness * 0.5)
    .vLine(1)
    .hLine(-wall_length)
    .vLine(-1)
    .hLine(wall_length - 1.5)
    .vLine(-1)
    .hLine(1.5)
    .close()
    .extrude(40)
    .workplaneFromTagged("top")
    .workplane(offset=c.wall_thickness)
    .move(yDist=-teensy_thickness * 0.5)
    .vLine(-1)
    .hLine(-wall_length)
    .vLine(1)
    .hLine(wall_length - 1.5)
    .vLine(1)
    .hLine(1.5)
    .close()
    .extrude(40)
    .workplaneFromTagged("top")
    .workplane(offset=c.wall_thickness)
    .move(xDist=1.5)
    .rect(2 * c.wall_thickness + 1, c.shield_width - 5, forConstruction=True)
    .vertices()
    .rect(c.wall_thickness, 5)
    .extrude(5)
    .faces(">X[-2]")
    .workplane(centerOption="CenterOfMass")
    .move(xDist=-c.shield_width * 0.5 + 2.5)
    .hLine(c.shield_width - 5)
    .vertices()
    .circle(1.6)
    .cutThruAll()
)


ov.show(
    battery_mount,
    battery_in_case,
    colors=["darkgreen", "darkblue"],
)

# %%


engraved_column = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .extrude(
        c.shield_with_usb_height - c.slope_height * 2 + 2 * c.wall_thickness
    )
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter - c.wall_thickness * 2,
    )
    .cutThruAll()
)

ov.show(
    engraved_column,
    battery_mount,
    battery_in_case,
    colors=["darkgreen", "darkblue"],
    alphas=[0.7, 1],
)

# %%

plate_cut = (
    cq.Workplane("XY")
    .move(yDist=-50, xDist=battery_mount_inner_diameter * 0.5 - 2)
    .rect(100, 100, centered=False)
    .extrude(200)
    .union(
        cq.Workplane("XY")
        .move(yDist=-50, xDist=-battery_mount_inner_diameter * 0.5 + 2)
        .rect(-100, 100, centered=False)
        .extrude(200)
    )
)

ov.show(
    engraved_column.cut(plate_cut).union(battery_mount),
    engraved_column.intersect(plate_cut),
    battery_in_case,
    colors=["darkgreen", "darkblue"],
    alphas=[0.7, 0.7, 1],
)

# %%

pe_size = 4

pe_x_points = 3
pe_y_points = 12

pe_x_width = c.face_width - pe_size - 1
pe_x_step = pe_x_width / (pe_x_points - 1)

pe_y_size = (
    c.shield_with_usb_height
    + 2 * c.wall_thickness
    - 2 * c.slope_height
    - pe_size
    - 1
)
pe_y_step = pe_y_size / (pe_y_points - 1)

pe_points = [
    (x * pe_x_step, y * pe_y_step)
    for x in range(pe_x_points)
    for y in range(pe_y_points)
]

pi_size = 6

pi_x_points = pe_x_points - 1
pi_y_points = pe_y_points - 1

pi_x_size = c.face_width - 13
pi_x_step = pi_x_size / (pi_x_points - 1)

pi_y_size = (
    c.shield_with_usb_height + 2 * c.wall_thickness - 2 * c.slope_height - 15.5
)
pi_y_step = pi_y_size / (pi_y_points - 1)

pi_points = [
    (x * pi_x_step, y * pi_y_step)
    for x in range(pi_x_points)
    for y in range(pi_y_points)
]


def engrave(ec: cq.Workplane, face: str):
    ec = (
        ec.faces(face)
        .workplane(centerOption="CenterOfMass")
        .tag("start")
        .center(
            -pe_x_width * 0.5,
            -pe_y_size * 0.5,
        )
        .pushPoints(pe_points)
        .polygon(nSides=8, circumscribed=True, diameter=pe_size)
        .extrude(c.wall_thickness * 0.5, taper=30)
    )
    return (
        ec.workplaneFromTagged("start")
        .center(
            -pi_x_size * 0.5,
            -pi_y_size * 0.5,
        )
        .pushPoints(pi_points)
        .polygon(nSides=8, circumscribed=True, diameter=pi_size)
        .extrude(c.wall_thickness, taper=40)
    )


for f in c.faces:
    engraved_column = engrave(engraved_column, f"{f}[-2]")

ov.show(engraved_column)

# %%

battery_case_lid = engraved_column.intersect(plate_cut)

ov.show(battery_case_lid)

# %%

battery_case_lid.export("print_files/controller_case_lid_decorated.stl")

# %%

battery_case_assembly = engraved_column.cut(plate_cut).union(battery_mount)

battery_case_assembly.export(
    "print_files/controller_case_assembly_decorated.stl"
)

# %%
