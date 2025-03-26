# %%

import cadquery as cq
import ocp_vscode as ov

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

crystal_middle_diameter = 144
crystal_base_height = 34
crystal_middle_height = 55
crystal_top_height = 34

crystal_total_height = (
    crystal_base_height
    + crystal_middle_height
    + crystal_top_height
    + slope_height
    + 2
)

# %%

toad_base = (
    cq.Workplane("XY")
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
    .extrude(2)
)

ov.show(toad_base)

# %%

toad_base.export("print_files/toad_base.stl")

# %%
