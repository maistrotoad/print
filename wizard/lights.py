# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 16

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

cut_depth = -12


lights = (
    lights.faces(f"{faces[0]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * fraction, centered=False)
    .cutBlind(cut_depth)
)

lights = (
    lights.faces(f"{faces[1]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * fraction, centered=False)
    .cutBlind(cut_depth)
)


ov.show(lights)

# %%


lights = (
    lights.faces(f"{faces[2]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)

lights = (
    lights.faces(f"{faces[3]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)


ov.show(lights)

# %%


lights = (
    lights.faces(f"{faces[4]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)

lights = (
    lights.faces(f"{faces[5]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)


ov.show(lights)

# %%


lights = (
    lights.faces(f"{faces[6]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width, casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)

lights = (
    lights.faces(f"{faces[7]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width, -casing_height * 0.9, centered=False)
    .cutBlind(cut_depth)
)


ov.show(lights)

# %%

mid_beam_distance = staff_middle_diameter * 0.5 - 2 - 4
beam_thickness = 4 - tolerance * 2
beam_span = 16
beam_depth = -4

lights = (
    lights.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x=mid_beam_distance, y=0)
    .rect(beam_thickness, beam_span)
    .extrude(beam_depth)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x=-mid_beam_distance, y=0)
    .rect(beam_thickness, beam_span)
    .extrude(beam_depth)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x=0, y=mid_beam_distance)
    .rect(beam_span, beam_thickness)
    .extrude(beam_depth)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x=0, y=-mid_beam_distance)
    .rect(beam_span, beam_thickness)
    .extrude(beam_depth)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(rotate=(0, 0, 45))
    .moveTo(x=0, y=-mid_beam_distance)
    .rect(beam_span, beam_thickness)
    .extrude(beam_depth)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(rotate=(0, 0, 45))
    .moveTo(x=0, y=mid_beam_distance)
    .rect(beam_span, beam_thickness)
    .extrude(beam_depth)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(rotate=(0, 0, 45))
    .moveTo(x=mid_beam_distance, y=0)
    .rect(beam_thickness, beam_span)
    .extrude(beam_depth)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(rotate=(0, 0, 45))
    .moveTo(x=-mid_beam_distance, y=0)
    .rect(beam_thickness, beam_span)
    .extrude(beam_depth)
)

ov.show(lights)

# %%

lights.export("print_files/lights_extension.stl")


# %%

lights_for_mask = get_lights()

ov.show(lights_for_mask)

# %%

mask_depth = -4

lights_for_mask = (
    lights_for_mask.faces(f"{faces[6]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(x_offset, base_y - y_offset)
    .rect(strip_width - tolerance, casing_height * 0.9, centered=False)
    .cutBlind(mask_depth)
)

lights_for_mask = (
    lights_for_mask.faces(f"{faces[7]}[-2]")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(rotate=(0, 0, angle))
    .moveTo(-x_offset, top_y + y_offset)
    .rect(-strip_width + tolerance, -casing_height * 0.9, centered=False)
    .cutBlind(mask_depth)
)

lights_mask = get_lights().cut(lights_for_mask)

ov.show(lights_mask)

lights_mask.export("print_files/lights_mask.stl")

# %%
