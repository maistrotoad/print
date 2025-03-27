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

staff_middle_diameter = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2
casing_height = 75

casing_start_inner_diameter = 70

# %%

extra_margin = 1.6

ring_cut = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter + tolerance * 2,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter + tolerance * 2,
    )
    .extrude(slope_height * 0.4 + extra_margin)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter + tolerance * 2,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .loft(ruled=True)
)

ov.show(ring_cut)

# %%

# %%


ring_cap = (
    cq.Workplane("XY")
    .workplane(offset=-slope_height * 0.2)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + tolerance * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter + wall_thickness * 2,
    )
    .extrude(slope_height * 2 + wall_thickness + extra_margin)
    .cut(ring_cut)
)

ov.show(ring_cut, ring_cap, colors=["darkgreen", "darkblue"])

# %%

# %%


def add_knob_mount(wp, face):
    wp = (
        wp.faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(slope_height)
        .extrude(wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(slope_height * 1.5)
        .extrude(wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .tag("mount_face")
        .move(xDist=-slope_height * 1.5, yDist=slope_height)
        .rect(slope_height * 3, slope_height * 3, centered=False)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-slope_height * 1.5, yDist=-slope_height)
        .rect(slope_height * 3, -slope_height * 3, centered=False)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=slope_height * 1.5)
        .circle(wall_thickness * 0.5)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-slope_height * 1.5)
        .circle(wall_thickness * 0.5)
        .cutBlind(-wall_thickness)
    )
    return wp


ring_cap = add_knob_mount(ring_cap, "<X")
ring_cap = add_knob_mount(ring_cap, ">X")

ring_cap = ring_cap.cut(
    cq.Workplane("XY")
    .transformed(offset=(-60, -tolerance * 0.5, -2))
    .box(120, 120, 100, centered=False)
)

ov.show(ring_cap)

# %%

ring_cap.export("print_files/ring_cap_large_extra_margin.stl")

# %%
