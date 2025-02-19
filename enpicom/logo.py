# %%

import cadquery as cq
import ocp_vscode as ov

outer = cq.Workplane("XY").polygon(6, 21)

inner = cq.Workplane("XY").workplane(offset=8).polygon(3, 13)

inner2 = cq.Workplane("XY").workplane(offset=-8).polygon(3, 13)


point_a = inner.vertices("<X and <Y")

point_b = outer.vertices("<(1,1,0)")


ov.show(
    point_b,
    point_a.circle(1),
)

# %%

ov.show(
    outer,
    outer.vertices().sphere(1),
    inner,
    inner.vertices().sphere(1),
    inner2,
    inner2.vertices().sphere(1),
    inner.vertices("<X and <Y").sphere(2),
    outer.vertices("<(1,1,0)").sphere(2),
)

# %%
