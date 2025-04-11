# %%

import const as c
import cadquery as cq
import ocp_vscode as ov
from battery_interior import get_shield_cap

four_pack_base_length = 45.5
four_pack_depth = 8
four_pack_outer_length = 55

one_pack_length = 30
one_pack_width = 25

height = 110

# %%

battery_case = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_diameter - c.wall_thickness * 3,
    )
    .extrude(c.wall_thickness)
    .faces(">Z")
    .rect(
        one_pack_length + c.wall_thickness,
        one_pack_width + c.wall_thickness,
    )
    .rect(
        one_pack_length,
        one_pack_width,
    )
    .extrude(height - 10)
    .faces(">Z")
    .rect(
        one_pack_length + c.wall_thickness,
        one_pack_width + c.wall_thickness,
    )
    .workplane(offset=10)
    .rect(
        four_pack_base_length + c.wall_thickness,
        four_pack_base_length + c.wall_thickness,
    )
    .loft(ruled=True)
    .faces(">Z")
    .rect(
        one_pack_length,
        one_pack_width,
    )
    .cutBlind(-20)
    .faces(">Z")
    .rect(
        four_pack_base_length + c.wall_thickness,
        four_pack_base_length + c.wall_thickness,
    )
    .workplane(offset=four_pack_depth)
    .rect(
        four_pack_outer_length,
        four_pack_outer_length,
    )
    .loft(ruled=True)
    .faces(">Z")
    .rect(four_pack_base_length, four_pack_base_length)
    .cutBlind(-four_pack_depth)
)

bottom_cut = (
    cq.Workplane("XY")
    .workplane(offset=c.wall_thickness)
    .rect(
        one_pack_length + 2 * c.wall_thickness,
        one_pack_width - c.wall_thickness,
    )
    .rect(
        one_pack_width + 2 * c.wall_thickness,
        one_pack_length - c.wall_thickness,
    )
    .extrude(height - 10)
    .faces(">Z")
    .tag("start")
    .rect(
        one_pack_length + 2 * c.wall_thickness,
        one_pack_width - c.wall_thickness,
    )
    .workplane(offset=9)
    .rect(
        four_pack_base_length + 2 * c.wall_thickness,
        1,
    )
    .loft(ruled=True)
    .workplaneFromTagged("start")
    .workplane(offset=height - 10)
    .rect(
        one_pack_width + 2 * c.wall_thickness,
        one_pack_length - c.wall_thickness,
    )
    .workplane(offset=9)
    .rect(
        1,
        four_pack_base_length + 2 * c.wall_thickness,
    )
    .loft(ruled=True)
    .clean()
)

ov.show(battery_case, bottom_cut, colors=["darkgreen", "darkblue"])

# %%


battery_case = battery_case.cut(bottom_cut)
battery_case = battery_case.union(
    get_shield_cap().rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, 4))
)

ov.show(battery_case)

# %%

battery_case = (
    battery_case.faces(">Z")
    .rect(four_pack_outer_length, four_pack_outer_length)
    .rect(
        four_pack_outer_length - c.wall_thickness,
        four_pack_outer_length - c.wall_thickness,
    )
    .extrude(height)
)

ov.show(battery_case)


# %%


battery_case = (
    battery_case.faces(">Z")
    .rect(
        four_pack_outer_length - c.wall_thickness,
        four_pack_outer_length - c.wall_thickness,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_diameter + c.buldge_diameter,
    )
    .extrude(c.wall_thickness)
)

ov.show(battery_case)

# %%


top_cut = (
    cq.Workplane("XY")
    .workplane(offset=height + four_pack_depth + c.wall_thickness)
    .rect(
        four_pack_outer_length - 2 * c.wall_thickness,
        four_pack_outer_length + 2 * c.wall_thickness,
    )
    .rect(
        four_pack_outer_length + 2 * c.wall_thickness,
        four_pack_outer_length - 2 * c.wall_thickness,
    )
    .extrude(height - 2 * c.wall_thickness)
)

ov.show(battery_case, top_cut, colors=["darkgreen", "darkblue"])

# %%

battery_case = battery_case.cut(top_cut)

ov.show(battery_case)
# %%

support = (
    cq.Workplane("XY")
    .rect(
        four_pack_outer_length - c.wall_thickness * 2,
        four_pack_outer_length - c.wall_thickness * 2,
        forConstruction=True,
    )
    .vertices()
    .rect(3, 3)
    .extrude(height * 2 + 12)
)

battery_case = battery_case.union(support)

ov.show(battery_case)

# %%

battery_case.export("print_files/battery_case.stl")

# %%
