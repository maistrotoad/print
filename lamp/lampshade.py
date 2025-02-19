# %%

import cadquery as cq
import ocp_vscode as ov
import math

# %%

size = 180

box = cq.Workplane("XY").box(size, size, size).fillet(10)


ov.show(box)

# %%

face_name = ">X"

plus_size = size * 0.8
plus_width = plus_size * 0.25
plus_fillet = 5

depth = 2

face_0 = f"face_{face_name}_0"
face_1 = f"face_{face_name}_1"
face_2 = f"face_{face_name}_2"
face_3 = f"face_{face_name}_3"

# Large plus
box: cq.Workplane = (
    box.faces(face_name)
    .workplane(centerOption="CenterOfMass")
    .tag(face_0)
    .sketch()
    .rect(plus_size, plus_width)
    .rect(plus_width, plus_size)
    .clean()
    .vertices()
    .fillet(5)
    .finalize()
    .cutBlind(-depth)
)


def helix(r0, r_eps, p, h, d=0, frac=1e-1):
    def func(t):
        if t > frac and t < 1 - frac:
            z = h * t + d
            r = r0 + r_eps
        elif t <= frac:
            z = h * t + d * math.sin(math.pi / 2 * t / frac)
            r = r0 + r_eps * math.sin(math.pi / 2 * t / frac)
        else:
            z = h * t - d * math.sin(2 * math.pi - math.pi / 2 * (1 - t) / frac)
            r = r0 - r_eps * math.sin(
                2 * math.pi - math.pi / 2 * (1 - t) / frac
            )

        x = r * math.sin(-2 * math.pi / (p / h) * t)
        y = r * math.cos(2 * math.pi / (p / h) * t)

        return x, y, z

    return func


def thread(
    radius, pitch, height, d, radius_eps, aspect=10, N=100, deg=3, smooth=None
):
    e1_bottom = (
        cq.Workplane("XY")
        .parametricCurve(
            helix(radius, 0, pitch, height, -d),
            N=N,
            maxDeg=deg,
            smoothing=smooth,
        )
        .val()
    )
    e1_top = (
        cq.Workplane("XY")
        .parametricCurve(
            helix(radius, 0, pitch, height, d),
            N=N,
            maxDeg=deg,
            smoothing=smooth,
        )
        .val()
    )

    e2_bottom = (
        cq.Workplane("XY")
        .parametricCurve(
            helix(radius, radius_eps, pitch, height, -d / aspect),
            N=N,
            maxDeg=deg,
            smoothing=smooth,
        )
        .val()
    )
    e2_top = (
        cq.Workplane("XY")
        .parametricCurve(
            helix(radius, radius_eps, pitch, height, d / aspect),
            N=N,
            maxDeg=deg,
            smoothing=smooth,
        )
        .val()
    )

    f1 = cq.Face.makeRuledSurface(e1_bottom, e1_top)
    f2 = cq.Face.makeRuledSurface(e2_bottom, e2_top)
    f3 = cq.Face.makeRuledSurface(e1_bottom, e2_bottom)
    f4 = cq.Face.makeRuledSurface(e1_top, e2_top)

    sh = cq.Shell.makeShell([f1, f2, f3, f4])
    rv = cq.Solid.makeSolid(sh)

    return rv


thickness = 5
cylinder_diameter = 100
cylinder_radius = cylinder_diameter / 2
radius_eps = 2
radius = cylinder_radius - radius_eps
pitch = 10
height = 20
d = pitch / 3
eps = 0.2
radius_outer = radius + thickness + radius_eps


# Spiral cuts
def draw_spirals(box: cq.Workplane):
    max_i = 50
    max_depth = -2 * depth
    for i in range(max_i):
        angle_offset = i * 45
        angle_delta = 45 - (i / max_i * 30)
        radius_offset = i * 1.9
        rect_depth = max_depth + (i / max_i * depth * 1.9)
        rect_size = i * 0.25 + 0.5
        rect_width = rect_size - (i / max_i * 0.9)

        box: cq.Workplane = (
            box.workplaneFromTagged(face_0)
            .workplane(centerOption="CenterOfMass")
            .polarArray(10 + radius_offset, angle_offset, angle_delta, 1)
            .rect(rect_size, rect_width)
            .cutBlind(rect_depth)
        )

        angle_offset -= 120
        radius_offset *= 1.1

        rect_size *= 1.2 - 0.25
        box: cq.Workplane = (
            box.workplaneFromTagged(face_0)
            .workplane(centerOption="CenterOfMass")
            .polarArray(5 + radius_offset, angle_offset, -angle_delta, 1)
            .rect(rect_width, rect_size)
            .cutBlind(rect_depth)
        )

    return box


# Side-cut
inner_square = 50

mini_cross_size = 8
mini_cross_width = 6

box = (
    box.workplaneFromTagged(face_0)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width, 45)
    .rect(mini_cross_width, mini_cross_size, 45)
    .clean()
    .vertices()
    .fillet(0.2)
    .finalize()
    .cutBlind(-depth)
)

mini_cross_size = mini_cross_size * 0.7
mini_cross_width = mini_cross_size * 0.3

box = (
    box.faces(f"{face_name}[1]")
    .workplane(centerOption="CenterOfMass")
    .tag(face_1)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width)
    .rect(mini_cross_width, mini_cross_size)
    .clean()
    .vertices()
    .fillet(0.2)
    .finalize()
    .cutBlind(-depth)
)

# Box in plus sign
box_in_plus_size = plus_width * 0.8

box: cq.Workplane = (
    box.workplaneFromTagged(face_1)
    .sketch()
    .rect(box_in_plus_size, box_in_plus_size)
    .vertices()
    .fillet(plus_fillet)
    .finalize()
    .extrude(depth)
)

# Fat plus in box
fat_plus_size = box_in_plus_size * 0.8
fat_plus_width = fat_plus_size * 0.8

box: cq.Workplane = (
    box.workplaneFromTagged(face_0)
    .sketch()
    .rect(fat_plus_size, fat_plus_width)
    .rect(fat_plus_width, fat_plus_size)
    .clean()
    .vertices()
    .fillet(plus_fillet * 0.2)
    .finalize()
    .cutBlind(-depth)
)

# Bars in fat plus
bar_size = fat_plus_size * 0.55
bar_width = fat_plus_width * 0.2

points = [(-6, 0), (0, 0), (6, 0)]

box: cq.Workplane = (
    box.workplaneFromTagged(face_1)
    .pushPoints(points)
    .sketch()
    .rect(bar_width, bar_size)
    .vertices()
    .fillet(plus_fillet * 0.2)
    .finalize()
    .cutBlind(-depth)
)

box: cq.Workplane = (
    box.faces(f"{face_name}[1]")
    .workplane(centerOption="CenterOfMass")
    .tag(face_2)
    .pushPoints(points)
    .sketch()
    .rect(bar_width - 2, bar_size - 2)
    .vertices()
    .fillet(plus_fillet * 0.1)
    .finalize()
    .extrude(depth)
)

# Crosses in bars in fat plus
cross_size = 1
cross_width = cross_size * 0.2

box: cq.Workplane = (
    box.workplaneFromTagged(face_1)
    .transformed(offset=(0, 0, 0))
    .rarray(6, 3, 3, 3)
    .sketch()
    .rect(cross_size, cross_width, angle=45)
    .rect(cross_width, cross_size, angle=45)
    .clean()
    .vertices()
    .fillet(0.1)
    .finalize()
    .cutBlind(-depth)
)

# Bars in plus sign
bar_offset = plus_size * 0.45
bar_width = box_in_plus_size * 0.15


def bar_feature(box_in: cq.Workplane, xDist, yDist):
    sign = -1 * math.copysign(1, yDist if xDist == 0 else xDist)

    box_l = box_in_plus_size if xDist == 0 else bar_width
    box_h = bar_width if xDist == 0 else box_in_plus_size

    offset = (
        (0, yDist + (sign * 20), 0)
        if xDist == 0
        else (xDist + (sign * 20), 0, 0)
    )

    rarray = (0, 10, 1, 5) if xDist == 0 else (10, 0, 5, 1)

    box_in: cq.Workplane = (
        box_in.workplaneFromTagged(face_1)
        .transformed(offset=offset)
        .rarray(*rarray)
        .sketch()
        .rect(box_l, box_h)
        .vertices()
        .fillet(plus_fillet * 0.2)
        .finalize()
        .cutBlind(-depth)
    )

    box_in: cq.Workplane = (
        box_in.workplaneFromTagged(face_2)
        .transformed(offset=offset)
        .rarray(*rarray)
        .sketch()
        .rect(box_l - 2, box_h - 2)
        .vertices()
        .fillet(plus_fillet * 0.1)
        .finalize()
        .extrude(depth)
    )

    if yDist != 0:
        box_in = (
            box_in.workplaneFromTagged(face_1)
            .transformed(offset=offset)
            .rarray(5, 10, 5, 3)
            .circle(0.5)
            .cutBlind(-depth)
        )
    else:
        box_in = (
            box_in.workplaneFromTagged(face_1)
            .transformed(offset=offset)
            .rarray(10, 5, 3, 5)
            .circle(0.5)
            .cutBlind(-depth)
        )

    return box_in


box = bar_feature(box, 0, -bar_offset)

box = bar_feature(box, bar_offset, 0)

box = bar_feature(box, 0, bar_offset)

box = bar_feature(box, -bar_offset, 0)

# Mini pluses
mini_size = plus_size * (2 / 3)

mini_plus_size = mini_size * 0.5
mini_plus_width = mini_plus_size * 0.25

mini_plus_fillet = plus_fillet * 0.5

box = (
    box.workplaneFromTagged(face_0)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_plus_size, mini_plus_width)
    .rect(mini_plus_width, mini_plus_size)
    .clean()
    .vertices()
    .fillet(mini_plus_fillet)
    .finalize()
    .cutBlind(-depth)
)

box = (
    box.workplaneFromTagged(face_1)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_plus_size - 2, mini_plus_width - 2)
    .rect(mini_plus_width - 2, mini_plus_size - 2)
    .clean()
    .vertices()
    .fillet(mini_plus_fillet)
    .finalize()
    .extrude(depth)
)

box = (
    box.workplaneFromTagged(face_0)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_plus_size - 4, mini_plus_width - 4)
    .rect(mini_plus_width - 4, mini_plus_size - 4)
    .clean()
    .vertices()
    .fillet(mini_plus_fillet)
    .finalize()
    .cutBlind(-depth)
)

# Mini box in mini pluses
mini_box_in_mini_plus_size = mini_plus_width * 0.8
mini_box_in_mini_plus_width = mini_box_in_mini_plus_size * 0.6

box = (
    box.workplaneFromTagged(face_1)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_box_in_mini_plus_size, mini_box_in_mini_plus_width, -15)
    .rect(mini_box_in_mini_plus_width, mini_box_in_mini_plus_size, -15)
    .clean()
    .vertices()
    .fillet(mini_plus_fillet * 0.2)
    .finalize()
    .cutBlind(-depth)
)

# Micro box in mini box in mini pluses
micro_box = mini_box_in_mini_plus_width * 0.8

box = (
    box.workplaneFromTagged(face_2)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(micro_box, micro_box, -30)
    .vertices()
    .fillet(mini_plus_fillet * 0.2)
    .finalize()
    .cutBlind(-depth)
)

# Nano box in micro box in mini box in mini pluses
nano_box_size = micro_box * 0.8
nano_box_width = nano_box_size * 0.6

box = (
    box.faces(f"{face_name}[1]")
    .workplane(centerOption="CenterOfMass")
    .tag(face_3)
    .rect(mini_size, mini_size, forConstruction=True)
    .vertices()
    .sketch()
    .rect(nano_box_size, nano_box_width, -45)
    .rect(nano_box_width, nano_box_size, -45)
    .clean()
    .vertices()
    .fillet(mini_plus_fillet * 0.1)
    .finalize()
    .cutBlind(-depth)
)


def place_cross(
    box_in: cq.Workplane,
    square_x,
    square_y,
    mini_cross_size,
    mini_cross_width,
):
    box_in = (
        box_in.workplaneFromTagged(face_0)
        .rect(square_x, square_y, forConstruction=True)
        .vertices()
        .sketch()
        .rect(mini_cross_size, mini_cross_width, 45)
        .rect(mini_cross_width, mini_cross_size, 45)
        .clean()
        .vertices()
        .fillet(0.5)
        .finalize()
        .cutBlind(-depth)
    )

    box_in = (
        box_in.workplaneFromTagged(face_1)
        .rect(square_x, square_y, forConstruction=True)
        .vertices()
        .sketch()
        .rect(mini_cross_size - 1, mini_cross_width - 1, 45)
        .rect(mini_cross_width - 1, mini_cross_size - 1, 45)
        .clean()
        .vertices()
        .fillet(0.5)
        .finalize()
        .cutBlind(-depth)
    )

    box_in = (
        box_in.workplaneFromTagged(face_2)
        .rect(square_x, square_y, forConstruction=True)
        .vertices()
        .sketch()
        .rect(mini_cross_size - 3, mini_cross_width - 3, 45)
        .rect(mini_cross_width - 3, mini_cross_size - 3, 45)
        .clean()
        .vertices()
        .fillet(0.2)
        .finalize()
        .cutBlind(-depth)
    )

    return box_in


mini_cross_size = mini_plus_size * 0.25
mini_cross_width = mini_cross_size * 0.2

mini_cross_offset = (mini_plus_size - mini_plus_width) * 0.8

outer_square = mini_size + mini_cross_offset
inner_square = mini_size - mini_cross_offset

box = place_cross(
    box, outer_square, outer_square, mini_cross_size, mini_cross_width
)

box = place_cross(
    box, outer_square, inner_square, mini_cross_size, mini_cross_width
)

box = place_cross(
    box, inner_square, outer_square, mini_cross_size, mini_cross_width
)

mini_cross_width = mini_cross_size * 0.7

box = (
    box.workplaneFromTagged(face_0)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width)
    .rect(mini_cross_width, mini_cross_size)
    .clean()
    .vertices()
    .fillet(0.5)
    .finalize()
    .cutBlind(-depth)
)

mini_cross_size = mini_cross_size * 0.8
mini_cross_width = mini_cross_size * 0.4

box = (
    box.workplaneFromTagged(face_1)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width, 15)
    .rect(mini_cross_width, mini_cross_size, 15)
    .clean()
    .vertices()
    .fillet(0.5)
    .finalize()
    .cutBlind(-depth)
)

mini_cross_size = mini_cross_size * 0.55
mini_cross_width = mini_cross_size * 0.7

box = (
    box.workplaneFromTagged(face_2)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width, 30)
    .rect(mini_cross_width, mini_cross_size, 30)
    .clean()
    .vertices()
    .fillet(0.2)
    .finalize()
    .cutBlind(-depth)
)

mini_cross_size = mini_cross_size * 0.55
mini_cross_width = mini_cross_size * 0.2

box = (
    box.workplaneFromTagged(face_2)
    .rect(inner_square, inner_square, forConstruction=True)
    .vertices()
    .sketch()
    .rect(mini_cross_size, mini_cross_width, 45)
    .rect(mini_cross_width, mini_cross_size, 45)
    .clean()
    .vertices()
    .fillet(0.1)
    .finalize()
    .cutBlind(-depth)
)


ov.show(box)

# %%

box = draw_spirals(box)
ov.show(box)
# %%

cut_box = cq.Workplane("XY").box(size, size, size).translate((-10, 0, 0))

box = box.cut(cut_box)

ov.show(box)

# %%

box_bottom = box.rotate((0, 0, 0), (0, 0, 1), 90)

box_2 = box.rotate((0, 0, 0), (0, 0, 1), 180)

box = box.union(box_2)

box_2 = box.rotate((0, 0, 0), (0, 1, 0), 90)

box = box.union(box_2).union(box_bottom)

ov.show(box)
# %%

box = box.rotate((0, 0, 0), (1, 0, 0), -90)

ov.show(box)
# %%


inner_box = cq.Workplane("XY").box(size - 10, size - 10, size - 10)

box = box.union(inner_box).clean()

ov.show(box, box.faces(">Z"))
# %%

ov.show(box, box.faces(">Z[-1]"))

# %%

box = (
    box.faces(">Z[-1]")
    .workplane(centerOption="CenterOfMass")
    .circle(radius_outer - thickness)
    .cutBlind(-80)
)

box = box.cut(cq.Workplane("XY").sphere(75))

outer = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(radius_outer)
    .circle(radius_outer - thickness)
    .extrude(height + 1.75 * d)
)
th2 = thread(
    radius_outer - thickness + eps, pitch, height, d, -radius_eps, deg=6
)
outer_threaded = outer.union(cq.Compound.makeCompound([th2])).translate(
    (0, 0, d + 80)
)

box = box.union(outer_threaded)

ov.show(box)
box.clean().export("lampshade.stl")

# %%
