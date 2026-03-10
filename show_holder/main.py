# %%

import cadquery as cq
import ocp_vscode as ov

# %%

back_block = (
    cq.Workplane("XY")
    .workplane(offset=-6)
    .moveTo(15, -17.5)
    .rect(30, 25)
    .extrude(18)
)

back_block = back_block.edges(">Z and >Y").chamfer(7)

back_block = (
    back_block.faces(">Z")
    .translate((0, 2, 0))
    .rect(17, 0, forConstruction=True)
    .vertices()
    .cboreHole(5, 10, 12, depth=None)
)

ov.show(back_block)

# %%

bottom_part = (
    cq.Workplane("XY")
    .line(0, 60)
    .threePointArc((15, 75), (30, 60))
    .line(0, -60)
    .close()
    .extrude(5)
).translate((0, -25, -11))

bottom_part = (
    bottom_part.faces(">Z")
    .translate((0, -25, 0))
    .rect(17, 0, forConstruction=True)
    .vertices()
    .circle(2.5)
    .cutThruAll()
)

ov.show(back_block, bottom_part)

# %%

bottom_wall_part = (
    cq.Workplane("XZ")
    .line(0, -60)
    .threePointArc((15, -75), (30, -60))
    .line(0, 60)
    .close()
    .extrude(5)
).translate((0, 0, -11))

ov.show(back_block, bottom_part, bottom_wall_part)

# %%

bottom_wall_part = (
    (
        bottom_wall_part.faces("<Y")
        .translate((0, 0, 25))
        .rect(18.5, 0, forConstruction=True)
        .vertices()
        .cboreHole(5, 10, 2, depth=None)
    )
    .mirror(("XZ"))
    .translate((0, -25, 0))
)

bottom_part = bottom_part.union(bottom_wall_part)

diag_beam = (
    cq.Workplane("XY")
    .rect(30, 3)
    .extrude(3)
    .translate((15, -18.5, -14))
    .edges(">Y and <Z")
    .chamfer(2.9)
)

bottom_part = bottom_part.union(diag_beam)

ov.show(bottom_part, diag_beam)

# %%

horizontal_gutter = cq.Workplane("XZ").move(15, 12).circle(5).extrude(30)


ov.show(back_block, horizontal_gutter)

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
    .moveTo(0, -10)
    .lineTo(30, -10)
    .threePointArc((75.5, 37.5), (30, 85))
    .lineTo(0, 85)
    .threePointArc((-47.5, 37.5), (0, -10))
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
    .moveTo(0, -15)
    .lineTo(30, -15)
    .threePointArc((80.5, 37.5), (30, 90))
    .lineTo(0, 90)
    .threePointArc((-52.5, 37.5), (0, -15))
    .close()
    .loft(ruled=True)
)
ov.show(mount_outer, mount, colors=["darkgreen", "darkblue"], alphas=[1, 0.5])

# %%

product = mount_outer.cut(mount)

product = product.edges(">Z").fillet(0.9)

product = product.union(base.translate((0, 14, 0)))

ov.show(product)


# %%

cable_gutter = (
    cq.Workplane("XY")
    .workplane(offset=12)
    .moveTo(15, -32)
    .circle(5)
    .extrude(-100)
)

product = product.union(back_block).cut(cable_gutter).cut(horizontal_gutter)


bottom_part = bottom_part.translate((0, -5, 0))

bottom_part = bottom_part.cut(cable_gutter)

ov.show(product, bottom_part)

# %%

product.export("show_top.stl")

bottom_part.export("show_bottom.stl")

# %%
