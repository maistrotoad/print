# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 10

shield_width = 29.5
shield_board_height = 99.2
shield_height = 106
shield_thickness = 20
shield_board_thickness = 1.6
shield_spacing = 5

arduino_width = 55
arduino_board_height = 68.5
arduino_height = 75
arduino_thickness = 40

staff_diameter = 80

staff_middle_diameter = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2
casing_height = 200

faces = list(
    reversed(
        [
            ">X",
            ">(1,-1,0)",
            "<Y",
            ">(-1,-1,0)",
            "<X",
            ">(-1,1,0)",
            ">Y",
            ">(1,1,0)",
        ]
    )
)

# %%


def get_column():
    return (
        cq.Workplane("XY")
        .polygon(
            8,
            diameter=staff_middle_diameter,
            circumscribed=True,
        )
        .extrude(casing_height)
    )


column = get_column()

column_cut = get_column()

left_face = (
    column_cut.faces(faces[-4]).workplane(centerOption="CenterOfMass").val()
)

assert isinstance(left_face, cq.Vector)

mid_face = (
    column_cut.faces(faces[-3]).workplane(centerOption="CenterOfMass").val()
)
assert isinstance(mid_face, cq.Vector)


right_face = (
    column_cut.faces(faces[-2]).workplane(centerOption="CenterOfMass").val()
)
assert isinstance(right_face, cq.Vector)


left_cut = (
    cq.Workplane(
        cq.Plane(
            origin=left_face,
            normal=cq.Vector(-1, -1, 0),
        )
    )
    .rect(30, casing_height)
    .extrude(10)
)


def get_mid(mid_face: cq.Vector) -> cq.Workplane:
    return cq.Workplane(
        cq.Plane(
            origin=mid_face,
            xDir=cq.Vector(1, 0, 0),
            normal=cq.Vector(0, -1, 0),
        )
    )


mid = get_mid(mid_face).rect(30, casing_height).extrude(10)

right_cut = (
    cq.Workplane(cq.Plane(origin=right_face, normal=cq.Vector(1, -1, 0)))
    .rect(30, casing_height)
    .extrude(10)
)

cut = left_cut.union(right_cut)

ov.show(
    mid,
    cut,
    colors=["blue", "green"],
)

# %%

spacing = 5

max_ax = 5
max_ay = 39

points_a = [
    (
        x * spacing - ((max_ax - 1) * 0.5 * spacing),
        y * spacing - ((max_ay - 1) * 0.5 * spacing),
    )
    for x in range(max_ax)
    for y in range(max_ay)
]


max_bx = max_ax + 1
max_by = max_ay + 1

points_b = [
    (
        x * spacing - ((max_bx - 1) * 0.5 * spacing),
        y * spacing - ((max_by - 1) * 0.5 * spacing),
    )
    for x in range(max_bx)
    for y in range(max_by)
]

pattern_ex = (
    get_mid(mid_face)
    .pushPoints(points_a)
    .polygon(8, diameter=3, circumscribed=True)
    .extrude(1, taper=30)
)

ov.show(pattern_ex)

# %%

pattern_in = (
    get_mid(mid_face)
    .pushPoints(points_b)
    .polygon(8, diameter=3.5, circumscribed=True)
    .extrude(-1, taper=40)
)

ov.show(pattern_ex, pattern_in)
# %%
