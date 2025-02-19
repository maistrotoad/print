# %%
import cadquery as cq
import ocp_vscode as ov
import math

# %%

size = 150
thickness = 5


def get_triangle(size):
    ratio = 605 / size

    width = 605 / ratio
    l1 = 365 / ratio
    l2 = 360 / ratio

    triangle_sketch: cq.Sketch = (
        cq.Sketch()
        .segment((0, 0), (width, 0), "s_a")
        .segment((width, 0), (30, 30), "s_b")
        .segment((30, 30), (0, 0), "s_c")
        .constrain("s_a", "Fixed", None)
        .constrain("s_a", "s_b", "Coincident", None)
        .constrain("s_b", "s_c", "Coincident", None)
        .constrain("s_c", "s_a", "Coincident", None)
        .constrain("s_a", "Length", width)
        .constrain("s_b", "Length", l1)
        .constrain("s_c", "Length", l2)
        .solve()
        .assemble()
    )

    return (
        cq.Workplane("XZ")
        .transformed(offset=(-size / 2, 0, -size / 2))
        .placeSketch(triangle_sketch)
        .extrude(size)
    )


triangle_outer = get_triangle(size)

triangle_inner = get_triangle(size - thickness * 2)

triangle_solid = triangle_outer.cut(triangle_inner)

hole_outer_size = 10
hole_inner_size = 5
hole_depth = 0.5


triangle_solid = (
    triangle_solid.faces("<<Z[1] and <<X[1]")
    .workplane(centerOption="CenterOfMass")
    .move(yDist=-20, xDist=50)
    .cboreHole(hole_inner_size, hole_outer_size, hole_depth, depth=None)
)


triangle_solid = (
    triangle_solid.faces("<<Z[2]")
    .workplane(centerOption="CenterOfMass")
    .move(yDist=-20, xDist=-50)
    .cboreHole(hole_inner_size, hole_outer_size, hole_depth, depth=None)
)


triangle_solid = (
    triangle_solid.faces("<<Z[3]")
    .workplane(centerOption="CenterOfMass")
    .move(yDist=-20, xDist=50)
    .cboreHole(hole_inner_size, hole_outer_size, hole_depth, depth=None)
)


triangle_solid = (
    triangle_solid.faces("<<Z[3]")
    .workplane(centerOption="CenterOfMass")
    .move(yDist=-20, xDist=-50)
    .cboreHole(hole_inner_size, hole_outer_size, hole_depth, depth=None)
)

lamp_hole = cq.Workplane("XY").circle(50).extrude(100)

triangle_solid = triangle_solid.cut(lamp_hole)

ov.show(triangle_solid)

# %%

cylinder_diameter = 100
cylinder_radius = cylinder_diameter / 2

square_to_circle = (
    cq.Workplane(
        "XY",
        origin=triangle_solid.faces("<Z")
        .workplane(centerOption="CenterOfMass")
        .val(),
    )
    .rect(size, size)
    .workplane(offset=-80, centerOption="CenterOfMass")
    .circle(cylinder_radius)
    .loft(combine=True)
)

square_to_circle_inner = (
    cq.Workplane(
        "XY",
        origin=triangle_solid.faces("<Z")
        .workplane(centerOption="CenterOfMass")
        .val(),
    )
    .rect(size - thickness, size - thickness)
    .workplane(offset=-80, centerOption="CenterOfMass")
    .circle(cylinder_radius - thickness)
    .loft(combine=True)
)

square_to_circle = square_to_circle.cut(square_to_circle_inner)

ov.show(square_to_circle)

# %%


ceiling_mount = triangle_solid.union(square_to_circle)

rod_left = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -25, -100))
    .ellipse(10, 15)
    .extrude(200)
)

rod_right = (
    cq.Workplane("YZ")
    .transformed(offset=(0, -25, -100))
    .ellipse(10, 15)
    .extrude(200)
)

ceiling_mount = ceiling_mount.cut(rod_left).cut(rod_right)

ov.show(ceiling_mount, ceiling_mount.vertices("|Z"))

# %%

ceiling_mount = ceiling_mount.translate((0, 0, 80))

ov.show(ceiling_mount)

# %%


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


radius_eps = 2
radius = cylinder_radius - radius_eps
pitch = 10
height = 20
d = pitch / 3
eps = 0.2

inner = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(radius)
    .circle(radius - thickness)
    .extrude(height + 1.75 * d)
)

th1 = thread(radius - eps, pitch, height, d, radius_eps, deg=6)
th1 = cq.Compound.makeCompound([th1])
inner_threaded = (
    inner.union(th1)
    .translate((0, 0, d))
    .rotateAboutCenter((1, 0, 0), 180)
    .translate((0, 1, -height - 1.75 * d))
)

ov.show(ceiling_mount, inner_threaded)
# %%

ceiling_mount = ceiling_mount.union(inner_threaded).clean()

final = cq.Assembly().add(
    ceiling_mount, name="ceiling_mount", color=cq.Color("brown")
)

ov.show(final)

final.toCompound().export("ceiling_mount.3mf")

# %%

# radius_outer = radius + thickness + radius_eps

# outer = (
#     cq.Workplane("XY", origin=(0, 0, -d))
#     .circle(radius_outer)
#     .circle(radius_outer - thickness)
#     .extrude(height + 1.75 * d)
# )
# th2 = thread(radius_outer - thickness + eps, pitch, height, d, -radius_eps)
# outer_threaded = outer.union(cq.Compound.makeCompound([th2])).translate(
#     (0, 0, -height - 1)
# )

# ov.show(ceiling_mount, outer_threaded)

# %%
