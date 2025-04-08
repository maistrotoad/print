# %%

import cadquery as cq
import ocp_vscode as ov
import const as c

toad_base = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .extrude(2)
)

led_inlet = (
    cq.Workplane("XY")
    .move(xDist=-16)
    .rect(14, 14)
    .workplane(offset=6)
    .move(xDist=-8)
    .rect(6, 14)
    .workplane(offset=4)
    .move(xDist=-6)
    .rect(3, 14)
    .workplane(offset=8)
    .move(xDist=-5)
    .rect(2, 13)
    .workplane(offset=8)
    .move(xDist=-4)
    .rect(0.2, 13)
    .loft(ruled=True)
)
led_inlet = led_inlet.union(led_inlet.rotate((0, 0, 0), (0, 0, 1), 180))
led_inlet = led_inlet.union(led_inlet.rotate((0, 0, 0), (0, 0, 1), 90))

ov.show(toad_base, led_inlet)

# %%

toad = cq.importers.importStep("print_files/Toad_low_poly_v2.step")

toad: cq.Compound = toad.val()


toad = toad.shell(toad.faces(), thickness=-c.wall_thickness)

print(toad)

ov.show(toad)

# %%


toad = cq.Workplane("XY").union(toad)

toad = toad.cut(cq.Workplane("XY").box(120, 120, 25 * 2))

toad = toad.val().scale(2.5)

toad = cq.Workplane(obj=toad).translate((-61, -66.5, -56))

toad = toad.union(toad_base)

sphere_size = 30

sphere_cut = cq.Workplane("XY").sphere(sphere_size).translate((-10, -45, 100))

sphere_cut = sphere_cut.union(
    cq.Workplane("XY").sphere(sphere_size).translate((-10, 70, 55))
)


sphere_cut = sphere_cut.union(
    cq.Workplane("XY").sphere(sphere_size).translate((-75, 10, 70))
)

sphere_cut = sphere_cut.union(
    cq.Workplane("XY").sphere(sphere_size).translate((60, 10, 87))
)

toad = toad.cut(sphere_cut)

toad = toad.cut(led_inlet)

ov.show(toad, colors=["darkgreen"], alphas=[1])

# %%

toad.export("print_files/toad_on_base.stl")

# %%
