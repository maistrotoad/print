# %%

import cadquery as cq
import math
import ocp_vscode as ov

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


radius = 100
pitch = 10
height = 20
d = pitch / 3
radius_eps = 2
eps = 1e-2
thickness = 10
radius_outer = radius + thickness + radius_eps + 0.5

inner = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(radius)
    .circle(radius - thickness)
    .extrude(height + 1.75 * d)
)
th1 = thread(radius - eps, pitch, height, d, radius_eps, deg=6)
inner_threaded = inner.union(cq.Compound.makeCompound([th1])).rotateAboutCenter(
    (1, 0, 0), 180
)

inner_cover = (
    cq.Workplane("XY", origin=(0, 0, -d)).circle(radius_outer).extrude(-10)
)

inner_threaded = inner_threaded.union(inner_cover).translate(
    (radius * 2 + 30, 0, 0)
)

outer = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(radius_outer)
    .circle(radius_outer - thickness)
    .extrude(height + 1.75 * d)
)
th2 = thread(
    radius_outer - thickness + eps, pitch, height, d, -radius_eps, deg=6
)
outer_threaded = outer.union(cq.Compound.makeCompound([th2]))


outer_cover = (
    cq.Workplane("XY", origin=(0, 0, -d)).circle(radius_outer).extrude(-10)
)

outer_threaded = outer_threaded.union(outer_cover)


final = (
    cq.Assembly()
    .add(inner_threaded, name="inner", color=cq.Color("red"))
    .add(outer_threaded, name="outer", color=cq.Color("blue"))
)

ov.show(final)


final.toCompound().export("lamp.3mf")

# %%
