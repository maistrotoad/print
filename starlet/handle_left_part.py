# %%


import cadquery as cq
import ocp_vscode as ov

left_ring = (
    cq.Workplane("XZ").circle(5).circle(2.5).extrude(7).translate((0, 7, 5))
)


ov.show(left_ring)

left_attach = cq.Workplane("XY").rect(12, 12).extrude(10).circle(2).cutThruAll()

ov.show(left_attach)

bolt_cut = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .polygon(6, 5, circumscribed=True)
    .workplane(offset=5)
    .polygon(6, 7, circumscribed=True)
    .loft(ruled=True)
)

left_attach = left_attach.cut(bolt_cut).translate((0, -6, 0))

ov.show(left_attach)

left_assembly = left_ring.union(left_attach)

ov.show(left_assembly)

left_assembly.export("./print_files/left_assembly.stl")


# %%
