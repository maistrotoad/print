# %%

import cadquery as cq
import ocp_vscode as ov

hexagon_size = 55
triangle_size = hexagon_size * 0.6

sphere_radius = hexagon_size * 0.075
rod_radius = sphere_radius * 0.3

print(f"sphere_radius: {sphere_radius}\nrod_radius:{rod_radius}")

hexagon_middle = cq.Workplane("XY").polygon(6, hexagon_size)

height = (
    hexagon_middle.vertices("<(1,1,0)")
    .val()
    .distance(hexagon_middle.vertices("<(1,-1,0)").val())
)

triangle_top = (
    cq.Workplane("XY").workplane(offset=height * 0.5).polygon(3, triangle_size)
)

triangle_bottom = (
    cq.Workplane("XY").workplane(offset=-height * 0.5).polygon(3, triangle_size)
)


def get_vector(value: cq.Workplane):
    return value.workplane(centerOption="CenterOfMass").val()


def get_rod(point_a: cq.Workplane, point_b: cq.Workplane):
    plane_a = cq.Plane(
        origin=get_vector(point_a),
        normal=get_vector(point_a) - get_vector(point_b),
    )

    length = point_a.val().distance(point_b.val())

    insert_length = sphere_radius

    length -= insert_length * 0.9 * 2

    start_gap = insert_length * 0.2

    insert_length -= start_gap

    rod = (
        cq.Workplane(plane_a)
        .workplane(offset=-start_gap)
        .circle(rod_radius * 0.45)
        .workplane(offset=-insert_length * 0.3)
        .circle(rod_radius * 0.65)
        .workplane(offset=-insert_length * 0.6)
        .circle(rod_radius)
        .workplane(offset=-length)
        .circle(rod_radius)
        .workplane(offset=-insert_length * 0.6)
        .circle(rod_radius * 0.65)
        .workplane(offset=-insert_length * 0.3)
        .circle(rod_radius * 0.45)
        .loft(ruled=True)
    )
    return rod


rods_top = [
    get_rod(
        triangle_top.vertices("<X and <Y"), triangle_top.vertices("<X and >Y")
    ),
    get_rod(triangle_top.vertices("<X and <Y"), triangle_top.vertices(">X")),
    get_rod(triangle_top.vertices("<X and >Y"), triangle_top.vertices(">X")),
]

ov.show(rods_top)

# %%

rods_hexagon = [
    get_rod(
        hexagon_middle.vertices("<X"), hexagon_middle.vertices("<(1,-1,0)")
    ),
    get_rod(hexagon_middle.vertices("<X"), hexagon_middle.vertices("<(1,1,0)")),
    get_rod(
        hexagon_middle.vertices("<(1,1,0)"),
        hexagon_middle.vertices("<(-1,1,0)"),
    ),
    get_rod(
        hexagon_middle.vertices("<(-1,1,0)"), hexagon_middle.vertices(">X")
    ),
    get_rod(
        hexagon_middle.vertices(">X"), hexagon_middle.vertices("<(-1,-1,0)")
    ),
    get_rod(
        hexagon_middle.vertices("<(-1,-1,0)"),
        hexagon_middle.vertices("<(1,-1,0)"),
    ),
]

print(
    hexagon_middle.vertices("<X")
    .val()
    .distance(hexagon_middle.vertices(">X").val())
)

rods_bottom = [
    get_rod(
        triangle_bottom.vertices("<X and <Y"),
        triangle_bottom.vertices("<X and >Y"),
    ),
    get_rod(
        triangle_bottom.vertices("<X and <Y"), triangle_bottom.vertices(">X")
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"), triangle_bottom.vertices(">X")
    ),
]

rods_diagonal = [
    get_rod(
        triangle_top.vertices("<X and <Y"), hexagon_middle.vertices("<(1,1,0)")
    ),
    get_rod(triangle_top.vertices("<X and <Y"), hexagon_middle.vertices("<X")),
    get_rod(triangle_top.vertices("<X and >Y"), hexagon_middle.vertices("<X")),
    get_rod(
        triangle_top.vertices("<X and >Y"), hexagon_middle.vertices("<(1,-1,0)")
    ),
    get_rod(triangle_top.vertices(">X"), hexagon_middle.vertices(">X")),
    get_rod(triangle_top.vertices(">X"), hexagon_middle.vertices(">(1,1,0)")),
    get_rod(triangle_top.vertices(">X"), hexagon_middle.vertices(">(1,-1,0)")),
    get_rod(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices("<(1,1,0)"),
    ),
    get_rod(
        triangle_bottom.vertices("<X and <Y"), hexagon_middle.vertices("<X")
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"), hexagon_middle.vertices("<X")
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices("<(1,-1,0)"),
    ),
    get_rod(triangle_bottom.vertices(">X"), hexagon_middle.vertices(">X")),
    get_rod(
        triangle_bottom.vertices(">X"), hexagon_middle.vertices(">(1,1,0)")
    ),
    get_rod(
        triangle_bottom.vertices(">X"), hexagon_middle.vertices(">(1,-1,0)")
    ),
]

triangle_top = triangle_top.vertices().sphere(sphere_radius)
hexagon_middle = hexagon_middle.vertices().sphere(sphere_radius)
triangle_bottom = triangle_bottom.vertices().sphere(sphere_radius)


for r in rods_top:
    triangle_top = triangle_top.union(r)

for r in rods_hexagon:
    hexagon_middle = hexagon_middle.union(r)

for r in rods_bottom:
    triangle_bottom = triangle_bottom.union(r)

all_rods_diagonal = None

for r in rods_diagonal:
    if all_rods_diagonal is None:
        all_rods_diagonal = r
    else:
        all_rods_diagonal = all_rods_diagonal.union(r)

triangle_top = triangle_top.cut(all_rods_diagonal)
hexagon_middle = hexagon_middle.cut(all_rods_diagonal)
triangle_bottom = triangle_bottom.cut(all_rods_diagonal)

ov.show(
    triangle_top,
    hexagon_middle,
    triangle_bottom,
    all_rods_diagonal,
)

# %%


enpicom_3d = cq.Assembly()

enpicom_3d.add(triangle_top, color=cq.Color("red"))
enpicom_3d.add(hexagon_middle, color=cq.Color("red"))
enpicom_3d.add(triangle_bottom, color=cq.Color("red"))

for r in rods_diagonal:
    enpicom_3d.add(r, color=cq.Color("red"))

ov.show(enpicom_3d)

enpicom_3d.toCompound().export("enpicom_3d.3mf")

# %%
