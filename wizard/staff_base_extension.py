# %%

import const as c
import cadquery as cq
import ocp_vscode as ov

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
    .extrude(c.column_height - c.slope_height * 2)
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

pe_size = 4

pe_x_points = 3
pe_y_points = 20

pe_x_width = c.face_width - pe_size - 1
pe_x_step = pe_x_width / (pe_x_points - 1)

pe_y_size = c.column_height - 2 * c.slope_height - pe_size - 1
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

pi_y_size = c.column_height - 2 * c.slope_height - 15.5
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
        .cutBlind(-c.wall_thickness, taper=40)
    )


for f in c.faces:
    engraved_column = engrave(engraved_column, f"{f}[-2]")


ov.show(engraved_column)

# %%


engraved_column.export("print_files/engraved_column.stl")

# %%
