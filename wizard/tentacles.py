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

tentacle_base = (
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
)

ov.show(tentacle_base)


# %%

pts = [(0, 0), (0, 150), (20, 200)]

# Spline path generated from our list of points (tuples)
path = cq.Workplane("XZ").spline(pts)

# Sweep a circle with a diameter of 1.0 units along the spline path we just created
solid_tentacle = (
    cq.Workplane("XY").rect(13, 18).sweep(path).translate((19.5, 0, 0))
)
solid_tentacle = solid_tentacle.union(
    solid_tentacle.rotate((0, 0, 0), (0, 0, 1), 180)
)
solid_tentacle = solid_tentacle.union(
    solid_tentacle.rotate((0, 0, 0), (0, 0, 1), 90)
)

tentacle_base = tentacle_base.cut(solid_tentacle)

ov.show(tentacle_base)

# %%

tentacle = (
    cq.Workplane("XY")
    .rect(10, 15)
    .rect(13, 18)
    .sweep(path)
    .translate((19.5, 0, 0))
)
tentacle = tentacle.union(
    cq.Workplane(
        cq.Plane(
            origin=tentacle.faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .val(),
            normal=cq.Vector(1, 0, 1),
        )
    )
    .workplane(offset=-0.5)
    .rect(13, 18)
    .extrude(3)
)

ov.show(tentacle)

# %%

tentacle = tentacle.union(tentacle.rotate((0, 0, 0), (0, 0, 1), 180))
tentacle = tentacle.union(tentacle.rotate((0, 0, 0), (0, 0, 1), 90))


tentacle_base = tentacle_base.union(tentacle)


ov.show(tentacle_base)

# %%

tentacle_base.export("print_files/tentacle_base.stl")

# %%
