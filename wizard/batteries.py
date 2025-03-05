# %%

import cadquery as cq
import ocp_vscode as ov
from math import sin, cos, pi


def helix(r0, r_eps, p, h, d=0, frac=1e-1):
    def func(t):
        if t > frac and t < 1 - frac:
            z = h * t + d
            r = r0 + r_eps
        elif t <= frac:
            z = h * t + d * sin(pi / 2 * t / frac)
            r = r0 + r_eps * sin(pi / 2 * t / frac)
        else:
            z = h * t - d * sin(2 * pi - pi / 2 * (1 - t) / frac)
            r = r0 - r_eps * sin(2 * pi - pi / 2 * (1 - t) / frac)

        x = r * sin(-2 * pi / (p / h) * t)
        y = r * cos(2 * pi / (p / h) * t)

        return x, y, z

    return func


def thread(wp: cq.Workplane, radius, pitch, height, d, radius_eps, aspect=10):
    e1_bottom = wp.parametricCurve(helix(radius, 0, pitch, height, -d)).val()
    e1_top = wp.parametricCurve(helix(radius, 0, pitch, height, d)).val()

    e2_bottom = wp.parametricCurve(
        helix(radius, radius_eps, pitch, height, -d / aspect)
    ).val()
    e2_top = wp.parametricCurve(
        helix(radius, radius_eps, pitch, height, d / aspect)
    ).val()

    f1 = cq.Face.makeRuledSurface(e1_bottom, e1_top)
    f2 = cq.Face.makeRuledSurface(e2_bottom, e2_top)
    f3 = cq.Face.makeRuledSurface(e1_bottom, e2_bottom)
    f4 = cq.Face.makeRuledSurface(e1_top, e2_top)

    sh = cq.Shell.makeShell([f1, f2, f3, f4])
    rv = cq.Solid.makeSolid(sh)

    return rv


pitch = 1.2
height = 4
d = pitch / 4
radius_eps = 0.2
base_radius = 6
outer_radius = base_radius + radius_eps * 2
eps = 0.1

core_inside = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(base_radius - eps)
    .extrude(height + 1.75 * d)
)
thread_outside = thread(
    cq.Workplane("XY"), base_radius - eps, pitch, height, d, radius_eps
)
thread_outside = core_inside.union(thread_outside)


core_outside = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(base_radius + radius_eps)
    .circle(base_radius + radius_eps * 2)
    .extrude(height + 1.75 * d)
)
thread_inner = thread(
    cq.Workplane("XY"), base_radius + radius_eps, pitch, height, d, -radius_eps
)

thread_inner = core_outside.union(thread_inner)

ov.show(
    cq.Assembly()
    .add(
        thread_inner.translate((0, 0, height * 0.65)),
        color=cq.Color(0, 0.5, 0, 1),
    )
    .add(thread_outside, color=cq.Color(0, 0, 0.5, 1))
)


# %%

wall_thickness = 2

shield_width = 29.5
shield_height = 106
shield_thickness = 20
shield_board_thickness = 1.6
shield_spacing = 5

arduino_width = 55
arduino_height = 75
arduino_thickness = 40

# Placing an arduino + shield
# Placing 2 shields back to back with spacing
# Placing another set bove it

base_diameter = 2 * wall_thickness + 2 * shield_thickness + shield_spacing

base_height = arduino_height + shield_height * 2 + shield_spacing

print(f"base_diameter: {base_diameter} base_height: {base_height}")

overhang_height = 20

battery_base_bottom = (
    cq.Workplane("XY")
    .polygon(8, base_diameter, circumscribed=True)
    .extrude(wall_thickness)
    .polygon(8, base_diameter, circumscribed=True)
    .polygon(8, base_diameter - 2 * wall_thickness, circumscribed=True)
    .extrude(base_height * 0.75)
    .translate((0, 0, -base_height * 0.75 - wall_thickness + overhang_height))
)

ov.show(battery_base_bottom)

# %%


battery_base_overhang = (
    cq.Workplane("XY")
    .polygon(8, base_diameter + 2 * radius_eps, circumscribed=True)
    .polygon(
        8,
        base_diameter + 2 * radius_eps + 2 * wall_thickness,
        circumscribed=True,
    )
    .extrude(overhang_height)
    .faces(">Z")
    .workplane()
    .polygon(8, base_diameter - 2 * wall_thickness, circumscribed=True)
    .polygon(
        8,
        base_diameter + 2 * radius_eps + 2 * wall_thickness,
        circumscribed=True,
    )
    .extrude(overhang_height)
)

ov.show(battery_base_bottom, battery_base_overhang)

# %%

battery_top_plane = (
    battery_base_overhang.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .val()
)

battery_base_top_outer = (
    cq.Workplane("XY", origin=battery_top_plane)
    .polygon(
        8,
        base_diameter + 2 * radius_eps + 2 * wall_thickness,
        circumscribed=True,
    )
    .workplane(offset=overhang_height)
    .polygon(8, base_diameter, circumscribed=True)
    .loft(ruled=True)
)

battery_base_top_inner = (
    cq.Workplane("XY", origin=battery_top_plane)
    .polygon(8, base_diameter - 2 * wall_thickness, circumscribed=True)
    .extrude(overhang_height)
)

ov.show(battery_base_top_outer, battery_base_top_inner)

# %%

battery_base_top = battery_base_top_outer.cut(battery_base_top_inner).union(
    battery_base_overhang
)

ov.show(battery_base_top)

# %%


battery_base_top = battery_base_top.faces(">Z").extrude(
    base_height * 0.25 - overhang_height * 2
)

colored = (
    cq.Assembly()
    .add(battery_base_bottom, color=cq.Color(0, 0.5, 0, 0.9))
    .add(battery_base_top, color=cq.Color(0, 0, 0.5, 0.9))
)

battery_base_top = (
    battery_base_top.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .move(yDist=-overhang_height * 0.5)
    .circle(outer_radius)
    .cutBlind(-10)
)

battery_base_bottom = (
    battery_base_bottom.faces(">X")
    .workplane(centerOption="ProjectedOrigin")
    .move(yDist=overhang_height * 0.5)
    .tag("tpos_plus_x")
    .circle(outer_radius)
    .cutBlind(-10)
)

core_outside = (
    cq.Workplane(
        "ZY",
        origin=battery_base_bottom.workplaneFromTagged("tpos_plus_x").val(),
    )
    .transformed(offset=(overhang_height * 0.5, 0, 0))
    .circle(base_radius + radius_eps)
    .circle(base_radius + radius_eps * 2)
    .extrude(height + 1.75 * d)
)
thread_inner = thread(
    cq.Workplane(
        "ZY",
        origin=battery_base_bottom.workplaneFromTagged("tpos_plus_x").val(),
    ).transformed(offset=(overhang_height * 0.5, 0, 0)),
    base_radius + radius_eps,
    pitch,
    height,
    d,
    -radius_eps,
)
thread_inner = core_outside.union(thread_inner).cut(
    cq.Workplane("XY").box(
        base_diameter - wall_thickness * 2,
        base_diameter - wall_thickness * 2,
        base_diameter - wall_thickness * 2,
    )
)


ov.show(
    battery_base_bottom,
    thread_inner,
    cq.Assembly().add(battery_base_top, color=cq.Color(0, 0, 0.3, 0.5)),
)

# %%
