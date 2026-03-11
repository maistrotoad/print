# %%

import cadquery as cq
import cadquery.func as cf
import ocp_vscode as ov

# parameters
D = 5
H = 2 * D
S = H / 10
TH: int | float = S / 10

# %%


render_v = cf.offset(
    cf.text("V", 1, font="MesloLGS NF", kind="bold"), TH * 2
).moved(z=-TH * 0.5)

render_i = cf.offset(
    cf.text("I", 1, font="MesloLGS NF", kind="bold"), TH
).moved(x=0.31)

render_n = cf.offset(
    cf.text("N", 1, font="MesloLGS NF", kind="bold"), TH * 2
).moved(z=-TH * 0.5, x=0.72)

render_c = cf.offset(
    cf.text("C", 1, font="MesloLGS NF", kind="bold"), TH
).moved(x=1.08)

render_e = cf.offset(
    cf.text("E", 1, font="MesloLGS NF", kind="bold"), TH * 2
).moved(z=-TH * 0.5, x=1.48)

render_n2 = cf.offset(
    cf.text("N", 1, font="MesloLGS NF", kind="bold"), TH
).moved(x=1.83)

render_t = cf.offset(
    cf.text("T", 1, font="MesloLGS NF", kind="bold"), TH * 2
).moved(z=-TH * 0.5, x=2.202)

vincent = cq.Workplane(
    cf.compound(
        render_v, render_i, render_n, render_c, render_e, render_n2, render_t
    )
)

ring = (
    cq.Workplane("XY")
    .circle(S * 0.2)
    .circle(S * 0.1)
    .extrude(TH * 2)
    .translate((-0.255, 0, -TH * 0.5))
)

vincent = vincent.union(ring)

ov.show(vincent)

# %%


vincent.export("vincent.stl")
# %%
