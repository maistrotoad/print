# %%


import cadquery as cq
import ocp_vscode as ov

right_ring = (
    cq.Workplane("XZ").circle(5).circle(2.5).extrude(7).translate((0, 0, 5))
)


ov.show(right_ring)

# %%

hinge = cq.Workplane("XY").rect(10, 10).extrude(22).translate((0, 5, 0))

hinge = (
    hinge.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .move(0, 6)
    .rect(10, 10)
    .extrude(12.5)
)

hinge = hinge.faces("<Z[-2]").edges(">X").fillet(3)

hinge = hinge.faces(">Z").edges(">X").fillet(5)

ov.show(
    right_ring,
    hinge,
)

# %%

hinge_ring = cq.Workplane("XZ").circle(7).extrude(10)

ov.show(hinge_ring)

# %%

hinge_ring = hinge_ring.translate((-18, 10, 19))


hinge_ring_holed = hinge_ring.faces("<Y").cboreHole(7, 10, 5, depth=None)

ov.show(hinge_ring_holed)

# %%


ov.show(hinge, hinge_ring)

# %%


hinge = hinge.cut(hinge_ring).union(hinge_ring_holed)

ov.show(hinge)

# %%

right_attach = (
    cq.Workplane("XY").rect(12, 12).extrude(10).circle(2).cutThruAll()
)

ov.show(right_attach)

bolt_cut = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .polygon(6, 5, circumscribed=True)
    .workplane(offset=5)
    .polygon(6, 7, circumscribed=True)
    .loft(ruled=True)
)

right_attach = right_attach.cut(bolt_cut).translate((0, 16, 0))

ov.show(right_attach)

right_assembly = right_ring.union(hinge).union(right_attach)

ov.show(right_assembly)

right_assembly.export("./print_files/right_assembly.stl")


# %%
