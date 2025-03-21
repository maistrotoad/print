# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 6

shield_width = 29.5
shield_board_height = 99.2
shield_height = 106
shield_thickness = 20
shield_board_thickness = 1.6
shield_spacing = 5

arduino_width = 55
arduino_board_height = 68.5
arduino_height = 75
arduino_thickness = 40

staff_diameter = 80

staff_middle_diameter = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2
casing_height = 200

casing_start_inner_diameter = 70

side_width = 20.72

strip_width = 12.5

# %%


def get_lights():
    return (
        cq.Workplane("XY")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter - wall_thickness * 2,
        )
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter + buldge_diameter,
        )
        .extrude(slope_height * 0.2)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter + buldge_diameter,
        )
        .workplane(offset=slope_height * 0.8)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter,
        )
        .loft(ruled=True)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter - wall_thickness * 2,
        )
        .cutBlind(-slope_height)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter - wall_thickness * 2,
        )
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter,
        )
        .extrude(casing_height - slope_height)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter,
        )
        .workplane(offset=slope_height * 0.8)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter + buldge_diameter,
        )
        .loft(ruled=True)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter + buldge_diameter,
        )
        .extrude(slope_height * 0.2)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter - wall_thickness * 2,
        )
        .cutBlind(-slope_height * 2)
    )


lights = get_lights()

faces = list(
    reversed(
        [
            ">X",
            ">(1,-1,0)",
            "<Y",
            ">(-1,-1,0)",
            "<X",
            ">(-1,1,0)",
            ">Y",
            ">(1,1,0)",
        ]
    )
)

base_y = -casing_height * 0.5
top_y = casing_height * 0.5

center_line_height = 24

angle = -5.6
x_offset = 3.25
y_offset = 3
fraction = 1


lights = (
    lights.faces(f"{faces[0]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * fraction, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[1]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * fraction, centered=False)
    .cutBlind(-4)
)

ov.show(lights)


# %%


lights = (
    lights.faces(f"{faces[2]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[3]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[4]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[5]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[6]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

lights = (
    lights.faces(f"{faces[7]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(-4)
)

ov.show(lights)

# %%
