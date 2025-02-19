# %%

import cadquery as cq
import ocp_vscode as ov

outer_diameter = 200.4
outer_radius = outer_diameter / 2

rim_thickness = 9.4
rim_to_glass = 1

case_thickness = 3
case_height = 38

case_wall = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius + case_thickness)
    .extrude(-case_height)
)

case_cap = (
    cq.Workplane("XY")
    .circle(outer_radius + case_thickness)
    .circle(outer_radius - rim_thickness - case_thickness)
    .extrude(case_thickness)
)

case_inner_wall = (
    cq.Workplane("XY")
    .circle(outer_radius - rim_thickness)
    .circle(outer_radius - rim_thickness - case_thickness)
    .extrude(-rim_to_glass)
)


case = (
    case_wall.union(case_cap)
    .union(case_inner_wall)
    .translate((0, 0, -case_thickness))
)

ov.show(case)


cog_thickness = 5

cog_teeth = (
    cq.Workplane("XY")
    .spline([(-10, outer_radius), (0, outer_radius + 20), (10, outer_radius)])
    .close()
    .extrude(cog_thickness)
)

for i in range(11):
    cog_teeth = cog_teeth.union(
        cog_teeth.rotate((0, 0, 0), (0, 0, 1), (i + 1) * 30)
    )

cog_wheel_rim = (
    cq.Workplane("XY")
    .circle(outer_radius + case_thickness)
    .circle(outer_radius - 2)
    .extrude(cog_thickness)
)

cog_wheel = cog_wheel_rim.union(cog_teeth)

ov.show(case, cog_wheel)

clock_case = (
    cq.Assembly()
    .add(case, name="case", color=cq.Color("black"))
    .add(cog_wheel, name="cog_wheel", color=cq.Color("red"))
)

ov.show(clock_case)

# %%

clock_case.toCompound().export("clock_case.3mf")

# %%
