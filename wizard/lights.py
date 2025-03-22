# %%

import cadquery as cq
import ocp_vscode as ov
from typing import Literal

wall_thickness = 10

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

strip_width = 12.5
global_cut_depth = -6
mask_depth = -4 + tolerance

# %%


def get_lights_core():
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
            diameter=staff_middle_diameter,
        )
        .extrude(casing_height)
    )


ov.show(get_lights_core())

# %%


def get_lights_caps():
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
        .extrude(casing_height - slope_height * 2)
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
    ).cut(get_lights_core())


ov.show(get_lights_caps())

# %%


r = staff_middle_diameter  # Radius of the helix
p = casing_height * 8  # Pitch of the helix
h = casing_height + 0.01  # Height of the helix

# Helix
wire = cq.Wire.makeHelix(pitch=p, height=h, radius=r)
helix = cq.Workplane(obj=wire)

helix_cut_top = (
    cq.Workplane("XY")
    .center(staff_middle_diameter * 0.5, 0)
    .rect(-12, strip_width * 0.6)
    .sweep(helix, isFrenet=True)
)
helix_cut_top = helix_cut_top.union(
    cq.Workplane("XY")
    .center(staff_middle_diameter * 0.5 + 2, 0)
    .rect(-8, strip_width * 0.8)
    .sweep(helix, isFrenet=True)
)
helix_cut_bottom = (
    cq.Workplane("XY")
    .center(staff_middle_diameter * 0.5 - 4.8, 0)
    .rect(-2.4, strip_width)
    .sweep(helix, isFrenet=True)
)
helix_cut = helix_cut_top.union(helix_cut_bottom)

ov.show(helix_cut, colors=["darkgreen"])

# %%

helix_cut = helix_cut.union(helix_cut.rotate((0, 0, 0), (0, 0, 1), 180))
helix_cut = helix_cut.union(helix_cut.rotate((0, 0, 0), (0, 0, 1), 90))

ov.show(helix_cut)

# %%

helix_cut_for_mask = (
    cq.Workplane("XY")
    .center(staff_middle_diameter * 0.5, 0)
    .rect((mask_depth + tolerance) * 2, strip_width * 0.6 - tolerance)
    .sweep(helix, isFrenet=True)
)
helix_cut_for_mask = helix_cut_for_mask.union(
    cq.Workplane("XY")
    .center(staff_middle_diameter * 0.5 + 2 - tolerance, 0)
    .rect((mask_depth + tolerance) * 2, strip_width * 0.8 - tolerance)
    .sweep(helix, isFrenet=True)
)

ov.show(helix_cut_for_mask)

# %%


helix_cut_for_mask = helix_cut_for_mask.union(
    helix_cut_for_mask.rotate((0, 0, 0), (0, 0, 1), 180)
)
helix_cut_for_mask = helix_cut_for_mask.union(
    helix_cut_for_mask.rotate((0, 0, 0), (0, 0, 1), 90)
)


lights_mask = get_lights_core().intersect(helix_cut_for_mask)

lights = get_lights_core().cut(helix_cut).union(get_lights_caps())

ov.show(
    lights,
    lights_mask,
    colors=["darkgreen"],
)

# %%

lights.export("print_files/lights_extension.stl")
lights_mask.export("print_files/lights_mask.stl")

# %%
