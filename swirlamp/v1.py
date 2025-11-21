# %%


import cadquery as cq
import ocp_vscode as ov

wire = cq.Wire.makeHelix(pitch=3, height=20, radius=5)
helix = cq.Workplane(obj=wire)

anti_wire = cq.Wire.makeHelix(pitch=-3, height=20, radius=5)
anti_helix = cq.Workplane(obj=anti_wire)


ov.show(helix, anti_helix)

# %%

helix_sweep = (
    cq.Workplane("XZ")
    .move(2.5, 2.5)
    .circle(0.4)
    .sweep(helix, sweepAlongWires=True)
)

anti_helix_sweep = (
    cq.Workplane("XZ")
    .move(3.5, 3.5)
    .circle(0.8)
    .sweep(anti_helix, sweepAlongWires=True)
)

ov.show(helix_sweep, anti_helix_sweep)

# %%

lamp_shade = (
    helix_sweep.union(
        helix_sweep.rotate((0, 0, 0), (0, 0, 1), 120).translate((0, 0, 0.5))
    )
    .union(helix_sweep.rotate((0, 0, 0), (0, 0, 1), 240).translate((0, 0, 1)))
    .union(anti_helix_sweep)
    .union(
        anti_helix_sweep.rotate((0, 0, 0), (0, 0, 1), 120).translate(
            (0, 0, 0.5)
        )
    )
    .union(
        anti_helix_sweep.rotate((0, 0, 0), (0, 0, 1), 240).translate((0, 0, 1))
    )
    .cut(cq.Workplane("XY").box(20, 20, 5).translate((0, 0, 24.25)))
)


ov.show(lamp_shade)

# %%
