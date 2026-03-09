# %%

import cadquery as cq
import ocp_vscode as ov
from thread import thread

# %%

base = cq.Workplane("XY").sphere(50)

to_cut = (
    cq.Workplane("XY")
    .workplane(offset=42.5)
    .circle(25)
    .circle(27.5)
    .extrude(10)
)

dots = (
    cq.Workplane("XY")
    .workplane(offset=37.5)
    .polygon(10, 51.25, forConstruction=True)
    .vertices()
    .circle(1.5)
    .extrude(15)
)

to_cut = to_cut.union(dots)

to_cut_assembly = to_cut.union(to_cut.rotate((0, 0, 0), (0, 1, 0), 90))

to_cut_assembly = to_cut_assembly.union(
    to_cut.rotate((0, 0, 0), (0, 1, 0), -90)
)
to_cut_assembly = to_cut_assembly.union(
    to_cut.rotate((0, 0, 0), (0, 1, 0), 180)
)


bottom_cut = cq.Workplane("XZ").workplane(offset=-35).circle(27.5).extrude(-25)

top_cut = cq.Workplane("XZ").workplane(offset=30).circle(37.5).extrude(25)

ov.show(base, top_cut, bottom_cut)

# %%


to_cut_assembly = to_cut_assembly.union(bottom_cut)

to_cut_assembly = to_cut_assembly.union(top_cut)


to_cut_assembly = to_cut_assembly.union(cq.Workplane("XY").sphere(48.5))


shade = base.cut(to_cut_assembly)

ov.show(shade)


# %%

radius = 33
pitch = 10
height = 17
d = pitch / 3
thread_height = height - 1.75 * d

radius_eps = 2
eps = 1e-2
thickness = 5
radius_outer = radius + thickness + radius_eps + 0.5

inner_top = (
    cq.Workplane("XZ", origin=(200, d, 0))
    .circle(radius)
    .circle(radius - thickness - 2)
    .extrude(-2)
)

inner_bottom = (
    cq.Workplane("XZ", origin=(200, d - height, 0))
    .circle(radius)
    .circle(radius - thickness - 2)
    .extrude(2)
)

inner_caps = inner_top.union(inner_bottom)

caps_left_cut = cq.Workplane("XY", origin=(170, 0, 0)).box(50, 50, 100)
caps_right_cut = cq.Workplane("XY", origin=(230, 0, 0)).box(50, 50, 100)

inner_caps = inner_caps.cut(caps_left_cut).cut(caps_right_cut)


# %%


inner = (
    cq.Workplane("XY", origin=(0, 0, -d - 2))
    .circle(radius)
    .circle(radius - thickness)
    .extrude(height + 4)
)
th1 = thread(radius - eps, pitch, thread_height, d, radius_eps, deg=6)
inner_threaded = inner.union(cq.Compound.makeCompound([th1])).rotateAboutCenter(
    (1, 0, 0), 180
)


outer = (
    cq.Workplane("XY", origin=(0, 0, -d))
    .circle(radius_outer)
    .circle(radius_outer - thickness)
    .extrude(height)
)
th2 = thread(
    radius_outer - thickness + eps, pitch, thread_height, d, -radius_eps, deg=6
)
outer_threaded = outer.union(cq.Compound.makeCompound([th2]))

inner_threaded = inner_threaded.rotate((0, 0, 0), (1, 0, 0), 90).translate(
    (200, 0, 0)
)
outer_threaded = outer_threaded.rotate((0, 0, 0), (1, 0, 0), 90).translate(
    (0, -30, 0)
)

shade = shade.union(outer_threaded)

inner_threaded = inner_threaded.union(inner_caps)


ov.show(shade, inner_threaded)

# %%

shade.export("sphere_shade_mount.stl")
inner_threaded.export("sphere_shade_inner_thread.stl")


# %%
