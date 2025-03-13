# %%

import cadquery as cq
import ocp_vscode as ov

epsilon = 0.2

thickness = 2.4

staff_diameter = 55

battery_module_height = 65 + 20

bottom_part_height = battery_module_height * 0.5 - thickness

bottom = (
    cq.Workplane("XY")
    .polygon(8, staff_diameter)
    .extrude(thickness)
    .polygon(8, staff_diameter)
    .polygon(8, staff_diameter - thickness * 2)
    .extrude(bottom_part_height)
)

top_diameter = staff_diameter - thickness * 2 - epsilon * 2

top = (
    cq.Workplane("XY", origin=(0, 0, bottom_part_height))
    .polygon(8, top_diameter)
    .polygon(8, top_diameter - thickness * 2)
    .extrude(battery_module_height * 0.5)
)

ov.show(bottom, top)

# %%
