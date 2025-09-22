# %%


import cadquery as cq
import ocp_vscode as ov

# %%

stand = (
    cq.Workplane("XY")
    .hLine(30)
    .vLine(3)
    .line(-20, 5)
    .vLine(-5)
    .hLine(-6)
    .vLine(30)
    .hLine(-4)
    .close()
    .extrude(50)
)

ov.show(stand)

stand.export("stand.stl")
# %%
