# %%

import math

import cadquery as cq
import const as c
import ocp_vscode as ov

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
    ring_cut = (
        cq.Workplane("XY")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d,
        )
        .workplane(offset=c.slope_height * 0.8)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.buldge_diameter + c.tolerance * 2,
        )
        .loft(ruled=True)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.buldge_diameter + c.tolerance * 2,
        )
        .extrude(c.slope_height * 0.4 + margin)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.buldge_diameter + c.tolerance * 2,
        )
        .workplane(offset=c.slope_height * 0.8)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d,
        )
        .loft(ruled=True)
    )

    ov.show(ring_cut)

    rc = (
        cq.Workplane("XY")
        .workplane(offset=-c.slope_height * 0.2)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.tolerance * 2,
        )
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=d + c.buldge_diameter + c.wall_thickness * 2,
        )
        .extrude(c.slope_height * 2 + c.wall_thickness + margin)
        .cut(ring_cut)
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
    hf = 6

    pd_a = 2
    xn_a = math.ceil(d / 9)
    yn_a = 2

    xs_a = wf - pd_a - 0.5
    xd_a = xs_a / (xn_a - 1)

    ys_a = hf - pd_a - 0.5
    yd_a = ys_a / (yn_a - 1)

    points_a = [(x * xd_a, y * yd_a) for x in range(xn_a) for y in range(yn_a)]

    pd_b = 3
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

    hf = 10
    yn_b = 3
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


ring_cap_large_2_2mm = get_ringcap(c.staff_diameter, 2.2)


ov.show(ring_cap_large_2_2mm)

ring_cap_large_2_2mm.export("print_files/ring_cap_large_2_2mm.stl")

# %%

ring_cap_small = get_ringcap(c.staff_middle_diameter, 0)
ring_cap_large = get_ringcap(c.staff_diameter, 0)


ov.show(
    ring_cap_small,
    ring_cap_large.translate((0, -40, 0)),
    colors=["darkgreen", "darkblue"],
)


# %%

ring_cap_small.export("print_files/ring_cap_small.stl")
ring_cap_large.export("print_files/ring_cap_large.stl")

# %%
