# %%

import cadquery as cq
import ocp_vscode as ov

# %%

thickness = 5

base_inner_diameter = 47
base_inner_radius = base_inner_diameter / 2

base_outer_radius = base_inner_radius + thickness

base_length = 25

knob_diameter = 20
knob_radius = knob_diameter / 2

shield = (
    cq.Workplane("XY")
    .circle(base_inner_radius)
    .circle(base_outer_radius)
    .extrude(base_length)
)

shield = (
    shield.workplane()
    .transformed(rotate=(0, 90, 0), offset=(base_outer_radius, 0, -2.5))
    .circle(knob_radius)
    .cutBlind(-thickness * 2)
)


mic_inner_diameter = 70
mic_inner_radius = mic_inner_diameter / 2
mic_outer_radius = mic_inner_radius + thickness

expanse_outer = (
    cq.Workplane(
        "XY",
        origin=shield.faces("<Z").workplane(centerOption="CenterOfMass").val(),
    )
    .circle(base_outer_radius)
    .workplane(offset=-5)
    .circle(mic_outer_radius)
    .loft(ruled=True, combine=False)
)

expanse_inner = (
    cq.Workplane(
        "XY",
        origin=shield.faces("<Z").workplane(centerOption="CenterOfMass").val(),
    )
    .circle(base_inner_radius)
    .workplane(offset=-5)
    .circle(mic_inner_radius)
    .loft(ruled=True, combine=False)
)

expanse = expanse_outer.cut(expanse_inner)

expanse_length = 100

expanse = (
    expanse.faces("<Z")
    .circle(mic_inner_radius)
    .circle(mic_outer_radius)
    .extrude(-expanse_length)
)

shield = shield.union(expanse).clean()

ov.show(shield)
# %%


shield.export("mic_shield.stl")

# %%
