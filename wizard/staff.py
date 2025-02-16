# %%
import cadquery as cq
import ocp_vscode as ov

staff_total_height = 1600  # mm

pole_height = 1450

pole_diameter = 40
pole_radius = pole_diameter / 2

pole_base_radius = 50
pole_base_height = 160

pole_height_remainder = pole_height - pole_base_height

pole = (
    cq.Workplane("XY")
    .circle(pole_base_radius)
    .workplane(offset=pole_base_height)
    .circle(pole_base_radius)
    .workplane(offset=0)
    .circle(pole_radius)
    .workplane(offset=pole_height_remainder)
    .circle(pole_radius)
    .loft(ruled=True)
)

ov.show(pole)


# %%

cap_base_height = 50
cap_radius = 50
cap_height = 100

cap = (
    cq.Workplane("XY")
    .workplane(offset=pole_height)
    .circle(pole_radius)
    .workplane(offset=cap_base_height)
    .circle(cap_radius)
    .workplane(offset=cap_height)
    .circle(cap_radius)
    .loft(ruled=True)
)

cap = cap.faces(">Z").extrude(10).edges(">Z").fillet(10)

ov.show(pole, cap)

# %%

offset = 40

twist_loft = (
    cq.Workplane("XY")
    .workplane(offset=pole_height - offset)
    .rect(10, 20)
    .workplane(offset=cap_base_height + offset)
    .transformed(rotate=(0, 0, 30))
    .move(0, cap_radius)
    .rect(10, 40)
    .workplane(offset=cap_height - offset)
    .transformed((0, 0, 30))
    .move(0, cap_radius)
    .rect(10, 60)
    .workplane(offset=cap_height)
    .transformed((0, 0, 30))
    .move(0, cap_radius)
    .rect(15, 80)
    .loft()
)

twist_loft = twist_loft.edges(">Z").fillet(4)

twist_loft = twist_loft.union(twist_loft.rotate((0, 0, 0), (0, 0, 1), 120)).union(
    twist_loft.rotate((0, 0, 0), (0, 0, 1), 240)
)

ov.show(twist_loft)

# %%


small_cap_radius = cap_radius - 5

small_cap = (
    cq.Workplane("XY")
    .workplane(offset=pole_height)
    .circle(pole_radius)
    .workplane(offset=cap_base_height)
    .circle(small_cap_radius)
    .workplane(offset=cap_height)
    .circle(cap_radius)
    .workplane(offset=cap_height * 2)
    .circle(cap_radius)
    .loft(ruled=True)
)

twist_loft = twist_loft.cut(small_cap)

cap = cap.cut(twist_loft)


cap_thickness = 8

cap_cutout = (
    cq.Workplane("XY")
    .workplane(offset=pole_height)
    .circle(pole_radius - cap_thickness)
    .workplane(offset=cap_base_height)
    .circle(cap_radius - cap_thickness)
    .workplane(offset=cap_height - cap_thickness)
    .circle(cap_radius - cap_thickness)
    .loft(ruled=True)
)

cap = cap.cut(cap_cutout)


ov.show(cap)

# %%

pole_thickness = 8

pole_cutout = (
    cq.Workplane("XY")
    .workplane(offset=pole_thickness)
    .circle(pole_base_radius - pole_thickness)
    .workplane(offset=pole_base_height - pole_thickness * 2)
    .circle(pole_base_radius - pole_thickness)
    .workplane(offset=0)
    .circle(pole_radius - pole_thickness)
    .workplane(offset=pole_height)
    .circle(pole_radius - pole_thickness)
    .loft(ruled=True)
)

pole = pole.union(twist_loft).clean().cut(pole_cutout).clean()

ov.show(pole)

# %%


final = (
    cq.Assembly()
    .add(pole, name="pole", color="gray")
    .add(cap, name="staff_cap", color="purple")
)

ov.show(final)

# %%
