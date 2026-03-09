# %%

import ocp_vscode as ov
import cadquery as cq
# %%

back_block = (
    cq.Workplane("XY")
    .workplane(offset=-6)
    .moveTo(15, -15)
    .rect(30, 20)
    .extrude(18)
)

back_block = back_block.edges(">Z and >Y").fillet(1)

back_block = (
    back_block.faces(">Z")
    .rect(20, 0, forConstruction=True)
    .vertices()
    .translate((0, 2, 0))
    .cboreHole(2.5, 5, 12, depth=None)
)

ov.show(back_block)


# %%

base = (
    cq.Workplane("XY")
    .lineTo(30, 0)
    .threePointArc((53.5, 23.5), (30, 47))
    .lineTo(0, 47)
    .threePointArc((-23.5, 23.5), (0, 0))
    .close()
    .extrude(2.5)
)

base = base.edges(">Z").fillet(1)

ov.show(base)


# %%

mount = (
    cq.Workplane("XY")
    .lineTo(30, 0)
    .threePointArc((67.5, 37.5), (30, 75))
    .lineTo(0, 75)
    .threePointArc((-37.5, 37.5), (0, 0))
    .close()
    .workplane(offset=12)
    .moveTo(0, -5)
    .lineTo(30, -5)
    .threePointArc((72.5, 37.5), (30, 80))
    .lineTo(0, 80)
    .threePointArc((-42.5, 37.5), (0, -5))
    .close()
    .loft(ruled=True)
)
ov.show(mount)


# %%


mount_outer = (
    cq.Workplane("XY")
    .workplane(offset=-6)
    .moveTo(0, -5)
    .lineTo(30, -5)
    .threePointArc((72.5, 37.5), (30, 80))
    .lineTo(0, 80)
    .threePointArc((-42.5, 37.5), (0, -5))
    .close()
    .workplane(offset=18)
    .moveTo(0, -10)
    .lineTo(30, -10)
    .threePointArc((75.5, 37.5), (30, 85))
    .lineTo(0, 85)
    .threePointArc((-47.5, 37.5), (0, -10))
    .close()
    .loft(ruled=True)
)
ov.show(mount_outer)

# %%

product = mount_outer.cut(mount).edges(">Z").fillet(1.5)

product = product.union(base.translate((0, 14, 0)))

ov.show(product)


# %%

cable_gutter = (
    cq.Workplane("XY")
    .workplane(offset=12)
    .moveTo(15, -25)
    .circle(5)
    .extrude(-100)
)

ov.show(product.union(back_block).cut(cable_gutter))

# %%
