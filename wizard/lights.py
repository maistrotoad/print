# %%

import cadquery as cq
import ocp_vscode as ov
from typing import Literal

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


global_cut_depth = -12


def cut_mask(
    wp: cq.Workplane,
    area: Literal["top"] | Literal["bottom"],
    cut_depth: int,
    tol: int,
):
    base_y = -casing_height * 0.5
    top_y = casing_height * 0.5

    angle = -5.6
    x_offset = 3.25 + tol
    y_offset = 3
    fraction = 1

    rect_width = strip_width - tol * 2
    rect_height = (casing_height * fraction) - tol * 2

    if area == "bottom":
        return (
            wp.workplane(centerOption="CenterOfBoundBox")
            .transformed(rotate=(0, 0, angle))
            .moveTo(x_offset, base_y - y_offset)
            .rect(rect_width, rect_height, centered=False)
            .cutBlind(cut_depth)
        )
    elif area == "top":
        return (
            wp.workplane(centerOption="CenterOfBoundBox")
            .transformed(rotate=(0, 0, angle))
            .moveTo(-x_offset, top_y + y_offset)
            .rect(-rect_width, -rect_height, centered=False)
            .cutBlind(cut_depth)
        )


def get_lights_cut(cut_depth: int = global_cut_depth, tol: int = 0):
    res = get_lights()
    a = "bottom"
    for f in faces:
        res = cut_mask(
            res.faces(f"{f}[-2]"), area=a, cut_depth=cut_depth, tol=tol
        )

        a = "top" if a == "bottom" else "bottom"

    return res


lights = get_lights_cut()


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

mask_depth = -4 + tolerance * 2

lights_for_mask = get_lights_cut(cut_depth=mask_depth, tol=tolerance)

ov.show(lights_for_mask)

# %%

ov.show(
    lights, lights_for_mask, colors=["darkgreen", "darkblue"], alphas=[0.1, 1]
)

# %%


lights_mask = get_lights().cut(lights_for_mask)

ov.show(lights_mask)

lights_mask.export("print_files/lights_mask.stl")

# %%
