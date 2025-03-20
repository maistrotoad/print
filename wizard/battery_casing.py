# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 2

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

housing_height = 220

starter_height = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2

casing_height = (
    wall_thickness
    + shield_height
    + 26
    + wall_thickness
    + wall_thickness
    + shield_board_height
    + wall_thickness
    + wall_thickness
)

print(f"casing_height: {casing_height}")


# %%


battery_casing = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height + wall_thickness)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .extrude(casing_height - slope_height)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8, circumscribed=True, diameter=staff_diameter + buldge_diameter
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height * 2)
)


def tag_wall(wp: cq.Workplane, face, pos, n, direction):
    depth = -1
    octa_distance = 3

    big_diameter = 16
    medium_diameter = 8
    small_diameter = 4

    y_offset = 0 if direction == 1 else 9

    y_offset = y_offset + n * 31

    bottom = -casing_height * 0.5 + slope_height + y_offset

    medium_x = octa_distance * 1.5 * direction
    medium_y = bottom + big_diameter * 0.5 + medium_diameter + octa_distance

    big_x = (-big_diameter * 0.5 + octa_distance * 0.5) * direction
    big_y = medium_y - (big_diameter * 0.5 + octa_distance) * direction

    small_x = (
        medium_x + (medium_diameter * 0.5 + octa_distance * 1.5) * direction
    )
    small_y = medium_y + (octa_distance * 1.5) * direction

    wp = (
        wp.faces(f"{face}[{pos}]")
        .workplane(centerOption="CenterOfMass")
        .tag("tag_start")
        .move(xDist=big_x, yDist=big_y)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=big_diameter,
        )
        .cutBlind(depth, taper=75)
        .workplaneFromTagged("tag_start")
        .move(xDist=medium_x, yDist=medium_y)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=medium_diameter,
        )
        .cutBlind(depth, taper=55)
        .workplaneFromTagged("tag_start")
        .move(xDist=small_x, yDist=small_y)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=small_diameter,
        )
        .cutBlind(depth, taper=35)
    )
    return wp


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

direction = 1

for i in range(13):
    n = int(i / 2)
    q = i % len(faces)
    r = (i + 4) % len(faces)

    battery_casing = tag_wall(
        battery_casing, faces[q], pos=-2, n=n, direction=direction
    )
    battery_casing = tag_wall(
        battery_casing, faces[r], pos=-2, n=n, direction=direction
    )

    direction *= -1

ov.show(battery_casing)

battery_casing.export("print_files/battery_casing.stl")

# %%
