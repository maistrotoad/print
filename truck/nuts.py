# %%

import ocp_vscode as ov
import cadquery as cq

truck_nuts = cq.Workplane("XY").sphere(30).translate((-25, -25, 0))

ov.show(truck_nuts)

# %%


bracket = (
    cq.Workplane("XY")
    .workplane(offset=-6)
    .moveTo(0, -50)
    .threePointArc((-50, -50), (-50, 0))
    .line(75, 50)
    .threePointArc((35, 50), (45, 20))
    .close()
    .extrude(12)
)

ov.show(truck_nuts, bracket)

# %%

truck_nuts = truck_nuts.union(bracket).translate((-30, -30, 0))

joint = (
    cq.Workplane("XY")
    .workplane(offset=-6)
    .circle(21)
    .circle(28)
    .extrude(6)
    .cut(
        cq.Workplane("XY")
        .workplane(offset=-10)
        .box(50, 60, 50)
        .translate((28.576, 0, 0))
    )
    .workplane()
    .move(0, -24.5)
    .line(0, 49, forConstruction=True)
    .vertices()
    .circle(2)
    .cutThruAll()
)

ov.show(joint)

# %%

truck_nuts = truck_nuts.cut(
    cq.Workplane("XY").workplane(offset=-6).circle(28).extrude(12)
)

truck_nuts = truck_nuts.union(joint).cut(
    cq.Workplane("XY")
    .workplane(offset=5)
    .box(10, 16, 10)
    .translate((0, -34, 0))
)

ov.show(truck_nuts)

# %%

ov.show(truck_nuts, truck_nuts.mirror((-1, 0, 0)).mirror((0, 0, -1)))

# %%

truck_nuts.export("./print_files/truck_nuts.stl")

# %%
