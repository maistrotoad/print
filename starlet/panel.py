# %%


import cadquery as cq
import ocp_vscode as ov

panel = cq.Workplane("XY").rect(155, 40).extrude(6)


panel = (
    panel.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .move(0, 12.5)
    .rect(130, 0, forConstruction=True)
    .vertices()
    .circle(2.5)
    .cutThruAll()
)

ov.show(panel)

# %%

panel = panel.edges("<Y").fillet(2)

ov.show(panel)

panel.export("./print_files/panel.stl")

# %%
