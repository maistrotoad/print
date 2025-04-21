# %%

import cadquery as cq
import const as c
import ocp_vscode as ov

weld_on = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter - 2 * c.wall_thickness,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter - 4 * c.wall_thickness,
    )
    .extrude(c.slope_height)
)

ov.show(weld_on)

weld_on.export("print_files/weld_on.stl")

# %%
