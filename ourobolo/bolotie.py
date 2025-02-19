# %%

import cadquery as cq
import ocp_vscode as ov

# %%

ov.config.set_viewer_config(transparent=False)

# Global settings
snake_radius = 5
snake_tail_radius = 1.5

body_rotate = 15


# Base for tie
tie_base = (
    cq.Workplane("XY")
    .hLine(15)
    .vLine(-10)
    .line(xDist=-12, yDist=-5)
    .hLine(-3)
    .vLine(7)
    .hLine(7)
    .vLine(2)
    .line(xDist=1, yDist=2)
    .line(xDist=3, yDist=1)
    .line(xDist=-3, yDist=1)
    .hLine(-3.5)
    .vLine(-2.5)
    .hLine(-2)
    .lineTo(2.5, 0)
    .close()
    .extrude(10)
)

ov.show(tie_base, tie_base.faces("<Z"))
# %%

tie_base_stabilizer = (
    tie_base.faces("<Z")
    .workplane()
    .move(xDist=2.5)
    .rect(12.5, 2, centered=False)
    .extrude(8)
)

ov.show(tie_base_stabilizer)
# %%

tie_base_stabilizer = tie_base_stabilizer.edges("|Y").fillet(0.9)


tie_base = tie_base.union(tie_base_stabilizer)

tie_base = tie_base.union(tie_base.mirror("YZ"))

ov.show(tie_base)
# %%

# Left start
left_arc = cq.Workplane("XZ").radiusArc((0, 30), 15)

left = cq.Workplane("YZ").circle(5).sweep(left_arc, isFrenet=True)

left = left.rotateAboutCenter((1, 0, 0), body_rotate)

left_last_face = left.faces("<Y").workplane(centerOption="CenterOfMass")

left_spline = left_last_face.spline(
    [(0, -12.5, 15), (0.75, -28.5, 30)],
    includeCurrent=True,
    tangents=[(0, 0, 1), (0, 0, 1)],
)

left_sweep = (
    cq.Workplane("XY")
    .pushPoints([left_spline.val().locationAt(0)])
    .circle(snake_radius)
    .pushPoints([left_spline.val().locationAt(1)])
    .circle(snake_tail_radius)
    .consolidateWires()
    .sweep(left_spline, multisection=True)
)

left_union = left.union(left_sweep).mirror("XY").clean()

ov.show(left_union)
# %%

left_face_val: cq.Vector = (
    left_union.faces(">Y").workplane(centerOption="CenterOfMass").val()
)

# Start adding scales
left_first_shrub_arc = (
    cq.Workplane("XZ", origin=left_face_val)
    .radiusArc((0, -30), -15)
    .rotateAboutCenter((1, 0, 0), -body_rotate)
    .translate((0, -3.5, 0))
)


def get_wp_at(arc, pos) -> cq.Workplane:
    loc: cq.Location = arc.val().locationAt(pos)
    return cq.Workplane("ZX", origin=loc.toTuple()[0]).transformed(
        rotate=(0, -15, -pos * 180 - 10), offset=(0.5, 0, -1.35)
    )


shrubs = None


def get_shrub_edge(pos: int) -> str:
    if pos < 0.2:
        return ">Z"
    elif pos < 0.6:
        return "<X"
    else:
        return "<Z"


max_i = 10
step = 1 / max_i

for i in range(max_i):
    pos = i * step
    height = 7 - 6 * pos
    item = (
        get_wp_at(left_first_shrub_arc, pos)
        .move(xDist=4.5, yDist=-5)
        .line(xDist=height, yDist=0)
        .line(xDist=-height, yDist=5)
        .close()
        .extrude(2)
        .edges(get_shrub_edge(pos))
        .fillet(0.5)
    )

    shrubs = item if shrubs is None else shrubs.union(item)

ov.show(left_union, shrubs)

# %%

left_union = left_union.union(shrubs)

# Start adding dragon faces

# Left face

left_face_top = (
    cq.Workplane("YZ", origin=left_face_val)
    .lineTo(-5, 0)
    .threePointArc((0, 5), (5, 0))
    .close()
)

left_face_top = (
    left_face_top.workplane(offset=2)
    .lineTo(-4, 0)
    .threePointArc((0, 4), (4, 0))
    .close()
    .loft(combine=True)
)

## Eyes location
eyes_start = cq.Workplane(
    "YX",
    origin=left_face_top.faces(">Z")
    .workplane(centerOption="CenterOfMass", offset=0.5)
    .val(),
)

left_eye_location = eyes_start.transformed(offset=(2.5, 0, -0.7))
right_eye_location = eyes_start.transformed(offset=(-2.5, 0, -0.7))

left_face_top = (
    left_face_top.workplane(offset=1)
    .lineTo(-4, 0)
    .threePointArc((0, 4), (4, 0))
    .close()
    .workplane(offset=1)
    .lineTo(-3.5, 0)
    .threePointArc((0, 2), (3.5, 0))
    .close()
    .loft(combine=True)
)

left_face_top = (
    left_face_top.workplane(offset=1.6)
    .lineTo(-3.5, 0)
    .threePointArc((0, 2), (3.5, 0))
    .close()
    .workplane(offset=6)
    .lineTo(-2, 0)
    .threePointArc((0, 1), (2, 0))
    .close()
    .loft(combine=True)
)

# Add eyes

left_eye = left_eye_location.sphere(1)

ov.show(left_face_top, left_eye)
# %%

left_iris = (
    cq.Workplane("ZY", origin=left_eye_location.val())
    .workplane(offset=-1)
    .circle(0.3)
    .extrude(1)
)

left_eye = left_eye.cut(left_iris)


right_eye = right_eye_location.circle(0.5).sphere(1)

right_iris = (
    cq.Workplane("ZY", origin=right_eye_location.val())
    .workplane(offset=-1)
    .circle(0.25)
    .extrude(1)
)

right_eye = right_eye.cut(right_iris)

# Left-face teeth
top_teeth_left = [(4.5, 1.7), (3.4, 2), (2.3, 2.3), (1.2, 2.6), (0.1, 2.9)]
top_teeth_right = [(i[0], -i[1]) for i in top_teeth_left]

top_teeth = None

for i in range(len(top_teeth_left)):
    depth = 1 - i * 0.1
    taper = 2 + i
    item = (
        left_face_top.faces("<Z")
        .workplane(centerOption="CenterOfMass")
        .pushPoints([top_teeth_left[i], top_teeth_right[i]])
        .circle(0.3)
        .extrude(depth, taper=taper)
    )

    top_teeth = item if top_teeth is None else top_teeth.union(item)


# Continue left-face
left_face_top = left_face_top.union(left_eye).union(right_eye).union(top_teeth)


left_face_top = left_face_top.edges(">X").fillet(0.2)

ov.show(left_face_top)
# %%

left_face_bottom = (
    cq.Workplane("YZ", origin=left_face_val)
    .lineTo(-5, 0)
    .threePointArc((0, -5), (5, 0))
    .close()
)

left_face_bottom = (
    left_face_bottom.workplane(offset=2)
    .moveTo(0, -2)
    .lineTo(-4, -2)
    .threePointArc((0, -4), (4, -2))
    .close()
    .loft(combine=True)
)

left_face_bottom = (
    left_face_bottom.workplane(offset=1.2)
    .moveTo(0, -2)
    .lineTo(-4, -2)
    .threePointArc((0, -4), (4, -2))
    .close()
    .workplane(offset=6)
    .moveTo(0, -6)
    .lineTo(-2, -6)
    .threePointArc((0, -7), (2, -6))
    .close()
    .loft(combine=True)
)

left_face_bottom = left_face_bottom.edges(">X").fillet(0.2)

ov.show(left_face_bottom)

# %%

bottom_teeth = None

bottom_teeth_left = [
    (1.7, -8),
    (2.0, -6.9),
    (2.3, -5.8),
    (2.6, -4.7),
    (2.9, -3.6),
]
bottom_teeth_right = [(-i[0], i[1]) for i in bottom_teeth_left]

for i in range(len(bottom_teeth_left)):
    depth = 1 - i * 0.1
    taper = 2 + i
    item = (
        left_face_bottom.faces(">Z")
        .workplane(centerOption="CenterOfMass", offset=-0.3)
        .transformed(rotate=(-10, 0, 0))
        .pushPoints([bottom_teeth_left[i], bottom_teeth_right[i]])
        .circle(0.3)
        .extrude(depth, taper=taper)
    )

    bottom_teeth = item if bottom_teeth is None else bottom_teeth.union(item)


left_face_bottom = left_face_bottom.union(bottom_teeth)


left_face = left_face_top.union(left_face_bottom).rotate(
    left_face_val,
    (left_face_val.x + 1, left_face_val.y, left_face_val.z),
    -body_rotate,
)

ov.show(left_face)

# %%

lace_face = left_face.translate((0, -4, 0)).rotate((0, 0, 0), (1, 0, 0), 15)

lace_face_start = lace_face.faces("<X").workplane(centerOption="CenterOfMass")


# Helix
lace_spline = lace_face_start.spline(
    [
        (0, 0, 0),
        (0, 0, 5),
        (2, 0, 10),
        (2, 2, 15),
        (0, 2, 20),
        (-2, 2, 25),
    ],
    tangents=[
        (0, 0, 1),
        (0, 0, 1),
    ],
)


ov.show(lace_spline)
# %%

lace_sweep = (
    cq.Workplane("XY")
    .pushPoints([lace_spline.val().locationAt(0)])
    .circle(5)
    .pushPoints([lace_spline.val().locationAt(1)])
    .circle(0.5)
    .consolidateWires()
    .sweep(lace_spline, multisection=True)
)

lace_face = lace_face.union(lace_sweep)

ov.show(lace_face)

# %%

left_horn_spline = (
    cq.Workplane("XY")
    .transformed(offset=(-2, -2, 0))
    .spline(
        [(-3, -4, 5), (-10, -4, 7)],
        includeCurrent=True,
        tangents=[(0, 0, 1), (-1, 0, 0)],
    )
)

horn_start_radius = 2
horn_end_radius = 0.5

left_lace_horn = (
    cq.Workplane("XY")
    .pushPoints([left_horn_spline.val().locationAt(0)])
    .circle(horn_start_radius)
    .pushPoints([left_horn_spline.val().locationAt(1)])
    .circle(horn_end_radius)
    .consolidateWires()
    .sweep(left_horn_spline, multisection=True)
)

left_lace_horn = left_lace_horn.edges("<X").fillet(0.5)

lace_horns = left_lace_horn.union(left_lace_horn.mirror("ZX"))

cylinder_cut = (
    cq.Workplane("YZ")
    .circle(2.3)
    .extrude(15)
    .translate((-2, 0, -2.3))
    .edges("<X")
    .fillet(1)
    .rotate((0, 0, 0), (0, 1, 0), 15)
    .translate((0, 0, 1.7))
)

ov.show(lace_face, cylinder_cut)

# %%

lace_face = (
    lace_face.union(lace_horns)
    .cut(cylinder_cut)
    .clean()
    .translate((0, 50, -13))
)

ov.show(lace_face)

# %%

left_union = left_union.union(left_face)

left_horn_spline = (
    cq.Workplane("XY")
    .transformed(offset=(-2, -2, 0))
    .spline(
        [(-3, -4, 5), (-10, -4, 7)],
        includeCurrent=True,
        tangents=[(0, 0, 1), (-1, 0, 0)],
    )
)

left_horn = (
    cq.Workplane("XY")
    .pushPoints([left_horn_spline.val().locationAt(0)])
    .circle(horn_start_radius)
    .pushPoints([left_horn_spline.val().locationAt(1)])
    .circle(horn_end_radius)
    .consolidateWires()
    .sweep(left_horn_spline, multisection=True)
)

left_horn = left_horn.edges("<X").fillet(0.5)

horns = (
    left_horn.union(left_horn.mirror("ZX"))
    .rotate((0, 0, 0), (1, 0, 0), -body_rotate)
    .translate((0, 4, 0))
)

left_union = left_union.union(horns).clean()

ov.show(left_union)

# %%


left_union = left_union.translate((-15, 0, 15))

right_union = left_union.mirror("YZ").mirror("XZ")

tie_base = tie_base.translate((0, 15, -5))

ourobolo = (
    cq.Assembly()
    .add(left_union.clean(), name="snake_a", color=cq.Color("blue"))
    .add(
        right_union.union(tie_base).clean(),
        name="snake_b",
        color=cq.Color("purple"),
    )
)

ourobolo_lace_end = cq.Assembly().add(
    lace_face, name="lace_face", color=cq.Color("blue")
)

ov.show(ourobolo, ourobolo_lace_end)

# %%
ourobolo.toCompound().export("ourobolo.3mf")

ourobolo_lace_end.toCompound().export("ourobolo_lace_end.3mf")

# %%
