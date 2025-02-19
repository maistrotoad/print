# %%

import cadquery as cq
import ocp_vscode as ov

# %%

thickness = 5
base_inner_diameter = 54.6  # 1mm margin
base_inner_radius = base_inner_diameter / 2
base_outer_radius = base_inner_radius + thickness


top_cap_height = 15

cap_height = 50

plateau_height = 15

base_mount = (
    cq.Workplane("XY")
    .circle(base_inner_radius)
    .circle(base_outer_radius)
    .extrude(cap_height)
    .faces(">Z")
    .circle(base_outer_radius)
    .extrude(plateau_height)
    .translate((0, 0, -cap_height - plateau_height))
)

cut_width = 25

cube_height = cap_height - top_cap_height

cube_cut = (
    cq.Workplane("XY")
    .box(cut_width, cut_width, cube_height)
    .translate(
        (
            0,
            -base_inner_radius,
            -0.5 * cube_height - top_cap_height - plateau_height,
        )
    )
)

base_mount = base_mount.cut(cube_cut)

ov.show(base_mount)
# %%

pole_inner_diameter = 16.5  # 1mm margin
pole_inner_radius = pole_inner_diameter / 2

pole_hole_diameter = 10  # diameter needed to screw on the pole
pole_hole_radius = pole_hole_diameter / 2

mount_thickness = 30

mount_height = 200

top_mount = (
    cq.Workplane("YZ")
    .hLine(-base_outer_radius)
    .vLine(mount_height)
    .hLine(mount_thickness)
    .vLine(-mount_height * 0.75)
    .lineTo(base_outer_radius, mount_thickness)
    .lineTo(base_outer_radius, 0)
    .close()
    .extrude(mount_thickness)
    .translate((-mount_thickness / 2, 0, 0))
)

top_mount = (
    top_mount.faces("<Y")
    .workplane()
    .pushPoints([(0, mount_height - mount_thickness / 2)])
    .circle(pole_inner_radius)
    .cboreHole(
        pole_hole_diameter,
        pole_inner_diameter,
        mount_thickness - 3,
        depth=None,
    )
)

cylinder_intersection = (
    cq.Workplane("XY").circle(base_outer_radius).extrude(mount_height)
)

top_mount = top_mount.intersect(cylinder_intersection)

mic_mount = base_mount.union(top_mount).clean()

ov.show(mic_mount)

mic_mount.export("mic_mount.stl")

# %%
