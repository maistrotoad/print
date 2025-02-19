# %%

import cadquery as cq
import ocp_vscode as ov

second_knob_diameter = 5.8
second_knob_radius = second_knob_diameter / 2

mini_cog_radius = second_knob_radius * 3

layer_thickness = 0.4

cog_teeth_bottom = (
    cq.Workplane("XY")
    .spline(
        [
            (-1.6, mini_cog_radius),
            (0, mini_cog_radius + 2.8),
            (1.6, mini_cog_radius),
        ]
    )
    .close()
    .extrude(-layer_thickness)
)

for i in range(11):
    cog_teeth_bottom = cog_teeth_bottom.union(
        cog_teeth_bottom.rotate((0, 0, 0), (0, 0, 1), (i + 1) * 30)
    )

cog_wheel = (
    cq.Workplane("XY")
    .circle(second_knob_radius - 0.2)
    .circle(mini_cog_radius + 0.2)
    .extrude(-layer_thickness)
)

cog_wheel = cog_wheel.union(cog_teeth_bottom)

ov.show(cog_wheel)

# %%

cog_teeth_top = (
    cq.Workplane("XY")
    .spline(
        [
            (-1.2, mini_cog_radius),
            (0, mini_cog_radius + 2.4),
            (1.2, mini_cog_radius),
        ]
    )
    .close()
    .extrude(layer_thickness)
)

for i in range(11):
    cog_teeth_top = cog_teeth_top.union(
        cog_teeth_top.rotate((0, 0, 0), (0, 0, 1), (i + 1) * 30)
    )

ov.show(cog_wheel, cog_teeth_top)

clock_second_cog = (
    cq.Assembly()
    .add(cog_wheel, name="cog_wheel", color=cq.Color("black"))
    .add(cog_teeth_top, name="cog_teeth_top", color=cq.Color("red"))
)

ov.show(clock_second_cog)

# %%

clock_second_cog.toCompound().export("clock_second_cog.3mf")

# %%
