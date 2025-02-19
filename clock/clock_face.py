# %%

import cadquery as cq
import ocp_vscode as ov

rim_thickness = 10

plate_diameter = 176
plate_radius = plate_diameter / 2

plate_thickness = 0.6

middle_hole_radius = 8

back_plate = (
    cq.Workplane("XY")
    .circle(plate_radius)
    .circle(middle_hole_radius)
    .extrude(-plate_thickness)
)

ov.show(back_plate)

# %%

mark_thickness = 0.4

five_min_mark = (
    cq.Workplane("XY")
    .move(0, plate_radius - 20)
    .rect(3, 16)
    .extrude(mark_thickness)
)

for i in range(12):
    if i == 0:
        continue
    five_min_mark = five_min_mark.union(
        five_min_mark.rotate((0, 0, 0), (0, 0, 1), (i) * 30)
    )

text = cq.Workplane("XY").text(
    "SCHAERLAECKENS",
    10,
    mark_thickness,
    fontPath="/usr/local/share/fonts/MonaspaceArgon-SemiBoldItalic.otf",
)

ov.show(back_plate, five_min_mark)
# %%

offset = 20

wrench = (
    cq.Workplane("XY")
    .move(0, middle_hole_radius + offset)
    .rect(4, 12)
    .extrude(mark_thickness)
)

wrench = wrench.union(
    cq.Workplane("XY")
    .move(0, middle_hole_radius + offset + 8)
    .circle(4)
    .extrude(mark_thickness)
)

wrench_cut = (
    cq.Workplane("XY")
    .move(0.5, middle_hole_radius + offset + 10.5)
    .rect(4, 6)
    .extrude(mark_thickness)
)

wrench = wrench.cut(wrench_cut)

ov.show(back_plate, five_min_mark, wrench)

# %%

min_mark = (
    cq.Workplane("XY")
    .move(0, plate_radius - 22)
    .rect(1, 8)
    .extrude(mark_thickness)
    .rotate((0, 0, 0), (0, 0, 1), 6)
)

for i in range(60):
    min_mark = min_mark.union(min_mark.rotate((0, 0, 0), (0, 0, 1), (i) * 6))


marks = five_min_mark.union(min_mark)

ov.show(back_plate, marks)

# %%

top = marks.union(wrench)

ov.show(back_plate, top)

final = (
    cq.Assembly()
    .add(back_plate.clean(), name="back_plate", color=cq.Color("red"))
    .add(top.clean(), name="top", color=cq.Color("black"))
)
ov.show(final)

final.toCompound().export("clock_face.3mf")

# %%
