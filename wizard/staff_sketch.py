# %%
import cadquery as cq
import ocp_vscode as ov

staff_total_height = 1600  # mm

pole_height = 1450

pole_diameter = 40
pole_radius = pole_diameter / 2


cap_base_height = 50
cap_radius = 50
cap_height = 100


def get_cap_base(radius: float, base_radius=pole_radius, end_radius=cap_radius):
    return (
        cq.Workplane("XY")
        .workplane(offset=pole_height)
        .circle(base_radius)
        .workplane(offset=cap_base_height)
        .polygon(6, radius * 2)
        .workplane(offset=cap_height)
        .polygon(6, end_radius * 2)
    )


cap = (
    get_cap_base(cap_radius)
    .workplane(offset=cap_base_height)
    .polygon(6, 1)
    .loft(ruled=True)
)


ov.show(cap)

# %%

offset = 40

twist_loft = (
    cq.Workplane("XY")
    .workplane(offset=pole_height - offset)
    .move(0, 15)
    .rect(10, 21)
    .workplane(offset=cap_base_height + offset)
    .transformed(rotate=(0, 0, 30))
    .move(0, cap_radius)
    .rect(10, 34)
    .workplane(offset=cap_height - offset)
    .transformed((0, 0, 30))
    .move(0, cap_radius)
    .rect(10, 55)
    .workplane(offset=cap_height)
    .transformed((0, 0, 30))
    .move(0, cap_radius)
    .rect(15, 89)
    .loft()
)

twist_loft = twist_loft.edges(">Z").fillet(4)

twist_loft = twist_loft.union(
    twist_loft.rotate((0, 0, 0), (0, 0, 1), 120)
).union(twist_loft.rotate((0, 0, 0), (0, 0, 1), 240))

ov.show(twist_loft)

# %%


small_cap_radius = cap_radius - 5

small_cap = (
    get_cap_base(small_cap_radius)
    .workplane(offset=cap_height * 2)
    .polygon(6, cap_radius * 2)
    .loft(ruled=True)
)

twist_loft = twist_loft.cut(small_cap)

cap = cap.cut(twist_loft)


cap_thickness = 8


cap_cutout = get_cap_base(
    cap_radius - cap_thickness,
    pole_radius - cap_thickness,
    cap_radius - cap_thickness,
).loft(ruled=True)

cap = cap.cut(cap_cutout)


ov.show(cap)

# %%

pole = (
    cq.Workplane("XY")
    .circle(pole_radius)
    .workplane(offset=pole_height)
    .circle(pole_radius)
    .loft(ruled=True)
)

ov.show(pole)


# %%

pole_thickness = 8

pole_cutout = (
    cq.Workplane("XY")
    .workplane(offset=pole_thickness)
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
    .add(pole, name="pole", color=cq.Color("gray"))
    .add(cap, name="staff_cap", color=cq.Color(1.0, 1.0, 1.0, 0.8))
)

ov.show(final)

# %%
