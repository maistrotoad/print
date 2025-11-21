# %%

import math

import cadquery as cq
import const as c
import ocp_vscode as ov

wall_thickness = 2

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
casing_height = 75

casing_start_inner_diameter = 70

# %%

battery_to_lights = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + 0.1,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + 0.1,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .workplane(offset=casing_height - slope_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + 0.1,
    )
    .loft(ruled=True)
)

battery_to_lights = battery_to_lights.union(
    battery_to_lights.mirror(("XY"))
).translate((0, 0, c.slope_height + 5))

ov.show(battery_to_lights)


# %%
def add_knob_mount(wp, face):
    wp = (
        wp.faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(c.slope_height)
        .extrude(c.wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(c.slope_height * 1.5)
        .extrude(c.wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .tag("mount_face")
        .move(xDist=-c.slope_height * 1.5, yDist=c.slope_height)
        .rect(c.slope_height * 3, c.slope_height * 3, centered=False)
        .cutBlind(-c.wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-c.slope_height * 1.5, yDist=-c.slope_height)
        .rect(c.slope_height * 3, -c.slope_height * 3, centered=False)
        .cutBlind(-c.wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=c.slope_height * 1.5)
        .circle(c.wall_thickness * 0.5)
        .cutBlind(-c.wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-c.slope_height * 1.5)
        .circle(c.wall_thickness * 0.5)
        .cutBlind(-c.wall_thickness)
    )
    return wp


def get_ringcap(d, margin):
    rc = (
        cq.Workplane("XY")
        .workplane(offset=-c.slope_height * 0.2)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d - 5,
        )
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.buldge_diameter + c.wall_thickness * 2,
        )
        .extrude(c.slope_height * 2 + c.wall_thickness + margin)
        .edges("(>X or >Y or <X or <Y) and (>Z or <Z)")
        .fillet(3)
        .rotate((0, 0, 0), (0, 0, 1), 45)
    )

    rc = add_knob_mount(rc, "<X")
    rc = add_knob_mount(rc, ">X")

    rc = rc.cut(
        cq.Workplane("XY")
        .transformed(offset=(-100, -c.tolerance * 0.5, -2))
        .box(300, 300, 300, centered=False)
    )

    wf = c.get_face_width(d + c.buldge_diameter + c.wall_thickness * 2)
    hf = 12

    pd_a = 2
    yn_a = 2
    xn_a = math.ceil(d / 9)

    xs_a = wf - pd_a - 0.5
    xd_a = xs_a / (xn_a - 1)

    ys_a = hf - pd_a - 0.5
    yd_a = ys_a / (yn_a - 1)

    points_a = [(x * xd_a, y * yd_a) for x in range(xn_a) for y in range(yn_a)]

    pd_b = 3
    yn_b = 3
    xn_b = xn_a - 1

    xs_b = wf - pd_b - 2 * pd_a - 0.25
    xd_b = xs_b / (xn_b - 1)

    points_b = [(x * xd_b, 0) for x in range(xn_b)]

    rc = (
        rc.faces("(1,-1,0)")
        .workplane(centerOption="CenterOfMass")
        .tag("start")
        .center(-xs_a * 0.5, -ys_a * 0.5)
        .pushPoints(points_a)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_a,
        )
        .extrude(1, taper=20)
    )

    rc = (
        rc.workplaneFromTagged("start")
        .center(-xs_b * 0.5, 0)
        .pushPoints(points_b)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_b,
        )
        .extrude(1.5, taper=25)
    )

    rc = (
        rc.faces("(-1,-1,0)")
        .workplane(centerOption="CenterOfMass")
        .tag("start")
        .center(-xs_a * 0.5, -ys_a * 0.5)
        .pushPoints(points_a)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_a,
        )
        .extrude(1, taper=20)
    )

    rc = (
        rc.workplaneFromTagged("start")
        .center(-xs_b * 0.5, 0)
        .pushPoints(points_b)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_b,
        )
        .extrude(1.5, taper=25)
    )

    rc = (
        rc.faces("(0,-1,0)")
        .workplane(centerOption="CenterOfMass")
        .tag("start")
        .center(-xs_a * 0.5, -ys_a * 0.5)
        .pushPoints(points_a)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_a,
        )
        .extrude(1, taper=20)
    )

    hf = 16
    ys_b = hf - pd_b - 0.5
    yd_b = ys_b / (yn_b - 1)

    points_b = [(x * xd_b, y * yd_b) for x in range(xn_b) for y in range(yn_b)]

    rc = (
        rc.workplaneFromTagged("start")
        .center(-xs_b * 0.5, -ys_b * 0.5)
        .pushPoints(points_b)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=pd_b,
        )
        .extrude(1.5, taper=25)
    )

    return rc


ring_cap_xl = get_ringcap(c.staff_diameter, 10)

ov.show(ring_cap_xl, battery_to_lights, colors=["darkgreen", "darkblue"])

# %%

ring_cap_xl = ring_cap_xl.cut(battery_to_lights)

ov.show(ring_cap_xl)

ring_cap_xl.export("print_files/ring_cap_xl.stl")
