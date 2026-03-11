# %%

import cadquery as cq
import cadquery.func as cf
import ocp_vscode as ov

# parameters
D = 5
H = 2 * D
S = H / 10
TH: int | float = S / 10
txt_a = "VNET"

txt_b = "ICN"

# planar
render_a = cf.text(txt_a, 1, font="MesloLGS NF", kind="bold")
render_b = cf.text(txt_b, 1, font="MesloLGS NF", kind="bold")

name_a = cf.offset(render_a, TH * 2).moved(z=-TH * 0.5)
name_b = cf.offset(render_b, TH)

ring = (
    cq.Workplane("XY")
    .circle(S * 0.2)
    .circle(S * 0.1)
    .extrude(TH)
    .translate((-1.16, 0, 0))
)

ov.show(name_a, name_b, ring)

# %%
