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

battery_to_lights = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=casing_start_inner_diameter,
    )
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
    .workplane(offset=casing_height - slope_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces("<Z[-2]")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=casing_start_inner_diameter,
    )
    .cutBlind(wall_thickness * 2)
)

cut_out = (
    cq.Workplane("XY")
    .workplane(offset=slope_height - wall_thickness)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .workplane(offset=casing_height + wall_thickness - slope_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - wall_thickness * 2,
    )
    .loft(ruled=True)
)

battery_to_lights = battery_to_lights.cut(cut_out)


ring_cut = (
    battery_to_lights.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .tag("slope_start")
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
        diameter=staff_middle_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter + tolerance * 2,
    )
    .extrude(slope_height * 0.4)
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


battery_to_lights = (
    battery_to_lights.faces(">Z")
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

ov.show(battery_to_lights)

# %%


ring_cap = (
    cq.Workplane("XY")
    .workplane(offset=casing_height - slope_height * 0.2)
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
    .extrude(slope_height * 2 + wall_thickness)
    .cut(ring_cut)
)

ov.show(ring_cut, ring_cap, colors=["darkgreen", "darkblue"])

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
    .transformed(offset=(-60, -tolerance * 0.5, 0))
    .box(120, 120, 100, centered=False)
)

ov.show(battery_to_lights, ring_cap, colors=["darkgreen", "darkblue"])

battery_to_lights.export("print_files/battery_to_lights.stl")

ring_cap.export("print_files/small_ring_cap.stl")

# %%
