# %%


import cadquery as cq
import ocp_vscode as ov

# %%

stand = (
    cq.Workplane("XY")
    .hLine(30)
    .vLine(1)
    .line(-5, 11)
    .vLine(-11)
    .hLine(-6)
    .vLine(10)
    .line(-19, -10)
    .close()
    .extrude(100)
)

stand = stand.edges(">Y").fillet(1)

stand = stand.edges(">Y").fillet(2)


ov.show(stand)

stand.export("stand.stl")
# %%
