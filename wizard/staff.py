# %%
import cadquery as cq
import ocp_vscode as ov

staff_total_height = 1600  # mm

pole_height = 1450

pole_diameter = 40
pole_radius = pole_diameter / 2

pole = cq.Workplane("XY").circle(pole_radius).extrude(pole_height)

ov.show(pole)


# %%

cap_base_height = 50
cap_radius = 50
cap_height = 100

staff_cap = (
    cq.Workplane("XY")
    .workplane(offset=pole_height)
    .circle(pole_radius)
    .workplane(offset=cap_base_height)
    .circle(cap_radius)
    .workplane(offset=cap_height)
    .circle(cap_radius)
    .loft(ruled=True)
)

ov.show(pole, staff_cap)

# %%

offset = 10

twist_loft = (
    cq.Workplane("XY")
    .workplane(offset=pole_height - offset)
    .rect(10, 20)
    .workplane(offset=cap_base_height + offset)
    .transformed(rotate=(0, 0, 30))
    .move(0, cap_radius)
    .rect(10, 60)
    .workplane(offset=cap_height + offset)
    .transformed((0, 0, 90))
    .move(0, cap_radius)
    .rect(10, 60)
    .loft()
)

twist_loft = twist_loft.union(twist_loft.rotate((0, 0, 0), (0, 0, 1), 120)).union(
    twist_loft.rotate((0, 0, 0), (0, 0, 1), 240)
)

twist_loft = twist_loft.cut(staff_cap)


ov.show(staff_cap, twist_loft)

# %%


final = (
    cq.Assembly()
    .add(pole, name="pole", color="gray")
    .add(staff_cap, name="staff_cap", color="purple")
    .add(twist_loft, name="twist_loft", color="gray")
)

ov.show(final)

# %%
