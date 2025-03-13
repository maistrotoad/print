# %%


import cadquery as cq
import ocp_vscode as ov

CQObject = cq.Vector | cq.Location | cq.Shape | cq.Sketch

size = 89
epsilon = 0.1

sphere_radius = size * 0.075
rod_radius = sphere_radius * 0.25

print(f"sphere_radius: {sphere_radius}\nrod_radius:{rod_radius}")

triangle_top = (
    cq.Workplane("XY").workplane(offset=size / 2.5).polygon(3, size * 0.5)
)

triangle_bottom = (
    cq.Workplane("XY").workplane(offset=-size / 2.5).polygon(3, size * 0.5)
)


def assert_is_vector(value: CQObject) -> cq.Vector:
    if not isinstance(value, cq.Vector):
        raise ValueError(f"Expected a vector, got: {value}")

    return value


def assert_is_vertex(value: CQObject) -> cq.Vertex:
    if not isinstance(value, cq.Vertex):
        raise ValueError(f"Expected a vertex, got: {value}")

    return value


def get_vector(value: cq.Workplane) -> cq.Vector:
    result = value.workplane(centerOption="CenterOfMass").val()
    return assert_is_vector(result)


def get_rod(
    point_a: cq.Workplane,
    point_b: cq.Workplane,
    should_cut: bool = False,
):
    plane_a = cq.Plane(
        origin=get_vector(point_a),
        normal=get_vector(point_a) - get_vector(point_b),
    )

    v_a = assert_is_vertex(point_a.val())
    v_b = assert_is_vertex(point_b.val())

    rod_sphere_radius = sphere_radius * 0.3

    rod_sphere_offset = sphere_radius - 0.5 * rod_sphere_radius

    sphere_top = (
        cq.Workplane(plane_a)
        .workplane(offset=-rod_sphere_offset)
        .sphere(rod_sphere_radius)
    )

    sphere_bottom = (
        cq.Workplane(plane_a)
        .workplane(offset=-v_a.distance(v_b) + rod_sphere_offset)
        .sphere(rod_sphere_radius)
    )

    rod = (
        cq.Workplane(plane_a)
        .workplane(offset=-rod_sphere_offset)
        .circle(rod_radius)
        .workplane(offset=-v_a.distance(v_b) + rod_sphere_offset * 2)
        .circle(rod_radius)
        .workplane(offset=-insert_length * 0.6)
        .circle(rod_radius * 0.65)
        .workplane(offset=-insert_length * 0.3)
        .circle(rod_radius * 0.45)
        .loft(ruled=True)
    )

    rod = rod.union(sphere_top).union(sphere_bottom)

    if should_cut:
        sphere_cut_bottom = (
            cq.Workplane(plane_a)
            .workplane(offset=-v_a.distance(v_b) + rod_sphere_offset * 1.09)
            .rect(rod_sphere_radius * 0.5, rod_sphere_radius * 2)
            .rect(rod_sphere_radius * 2, rod_sphere_radius * 0.5)
            .clean()
            .extrude(-rod_sphere_radius * 1.5)
        )
        rod = rod.cut(sphere_cut_bottom)

    return rod


def get_rod_to_cut(point_a: cq.Workplane, point_b: cq.Workplane):
    plane_a = cq.Plane(
        origin=get_vector(point_a),
        normal=get_vector(point_a) - get_vector(point_b),
    )

    v_a = assert_is_vertex(point_a.val())
    v_b = assert_is_vertex(point_b.val())

    rod_sphere_radius = sphere_radius * 0.30 + epsilon

    rod_sphere_offset = sphere_radius - 0.5 * rod_sphere_radius

    sphere_top = (
        cq.Workplane(plane_a)
        .workplane(offset=-rod_sphere_offset)
        .sphere(rod_sphere_radius)
    )

    sphere_bottom = (
        cq.Workplane(plane_a)
        .workplane(offset=-v_a.distance(v_b) + rod_sphere_offset)
        .sphere(rod_sphere_radius)
    )

    rod = (
        cq.Workplane(plane_a)
        .workplane(offset=-rod_sphere_offset)
        .circle(rod_radius)
        .workplane(offset=-v_a.distance(v_b) + rod_sphere_offset * 2)
        .circle(rod_radius)
        .loft()
    )

    return rod.union(sphere_top).union(sphere_bottom)


# %%

rods_top = [
    get_rod(
        triangle_top.vertices("<X and <Y"), triangle_top.vertices("<X and >Y")
    ),
    get_rod(triangle_top.vertices("<X and <Y"), triangle_top.vertices(">X")),
    get_rod(triangle_top.vertices("<X and >Y"), triangle_top.vertices(">X")),
]

ov.show(rods_top)

# %%

rods_top_to_hexagon = [
    get_rod(
        triangle_top.vertices("<X and <Y"),
        hexagon_middle.vertices("<(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices("<X and <Y"),
        hexagon_middle.vertices("<X"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices("<X and >Y"),
        hexagon_middle.vertices("<X"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices("<X and >Y"),
        hexagon_middle.vertices("<(1,-1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices(">(1,0,0)"),
        hexagon_middle.vertices(">(1,0,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices(">X"),
        hexagon_middle.vertices(">(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices("<X and >Y"),
        hexagon_middle.vertices(">(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices(">X"),
        hexagon_middle.vertices(">(1,-1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_top.vertices("<X and <Y"),
        hexagon_middle.vertices(">(1,-1,0)"),
        should_cut=True,
    ),
]

ov.show(rods_top_to_hexagon)

# %%

rods_top_to_cut = [
    get_rod_to_cut(
        triangle_top.vertices("<X and <Y"), hexagon_middle.vertices("<(1,1,0)")
    ),
    get_rod_to_cut(
        triangle_top.vertices("<X and <Y"), hexagon_middle.vertices("<X")
    ),
    get_rod_to_cut(
        triangle_top.vertices("<X and >Y"), hexagon_middle.vertices("<X")
    ),
    get_rod_to_cut(
        triangle_top.vertices("<X and >Y"), hexagon_middle.vertices("<(1,-1,0)")
    ),
    get_rod_to_cut(triangle_top.vertices(">X"), hexagon_middle.vertices(">X")),
    get_rod_to_cut(
        triangle_top.vertices(">X"), hexagon_middle.vertices(">(1,1,0)")
    ),
    get_rod_to_cut(
        triangle_top.vertices("<X and >Y"), hexagon_middle.vertices(">(1,1,0)")
    ),
    get_rod_to_cut(
        triangle_top.vertices(">X"), hexagon_middle.vertices(">(1,-1,0)")
    ),
    get_rod_to_cut(
        triangle_top.vertices("<X and <Y"), hexagon_middle.vertices(">(1,-1,0)")
    ),
]


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

rods_hexagon_to_bottom = [
    get_rod(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices("<(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices("<X"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices("<X"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices("<(1,-1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices(">X"),
        hexagon_middle.vertices(">X"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices(">X"),
        hexagon_middle.vertices(">(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices(">(1,1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices(">X"),
        hexagon_middle.vertices(">(1,-1,0)"),
        should_cut=True,
    ),
    get_rod(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices(">(1,-1,0)"),
        should_cut=True,
    ),
]

ov.show(rods_hexagon_to_bottom)

# %%

rods_bottom_to_cut = [
    get_rod_to_cut(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices("<(1,1,0)"),
    ),
    get_rod_to_cut(
        triangle_bottom.vertices("<X and <Y"), hexagon_middle.vertices("<X")
    ),
    get_rod_to_cut(
        triangle_bottom.vertices("<X and >Y"), hexagon_middle.vertices("<X")
    ),
    get_rod_to_cut(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices("<(1,-1,0)"),
    ),
    get_rod_to_cut(
        triangle_bottom.vertices(">X"), hexagon_middle.vertices(">X")
    ),
    get_rod_to_cut(
        triangle_bottom.vertices(">X"), hexagon_middle.vertices(">(1,1,0)")
    ),
    get_rod_to_cut(
        triangle_bottom.vertices("<X and >Y"),
        hexagon_middle.vertices(">(1,1,0)"),
    ),
    get_rod_to_cut(
        triangle_bottom.vertices(">X"), hexagon_middle.vertices(">(1,-1,0)")
    ),
    get_rod_to_cut(
        triangle_bottom.vertices("<X and <Y"),
        hexagon_middle.vertices(">(1,-1,0)"),
    ),
]

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

ov.show(rods_bottom)

# %%

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
    *rods_top,
    triangle_top,
    *rods_top_to_hexagon,
    *rods_hexagon,
    hexagon_middle,
    *rods_hexagon_to_bottom,
    *rods_bottom,
    triangle_bottom,
)

# %%


top_part = triangle_top

for r in rods_top:
    top_part = top_part.union(r)

for r in rods_top_to_hexagon:
    top_part = top_part.union(r)

ov.show(top_part)

# %%

for r in rods_hexagon:
    hexagon_middle = hexagon_middle.union(r)

bottom_part = triangle_bottom

for r in rods_hexagon_to_bottom:
    bottom_part = bottom_part.union(r)

for r in rods_bottom:
    bottom_part = bottom_part.union(r)


ov.show(bottom_part)
# %%

# Cut holes in hexagon
for r in rods_top_to_cut:
    hexagon_middle = hexagon_middle.cut(r)

for r in rods_bottom_to_cut:
    hexagon_middle = hexagon_middle.cut(r)

ov.show(hexagon_middle)

top_part.export("enpicom_3d_top.stl")
hexagon_middle.export("enpicom_3d_middle.stl")
bottom_part.export("enpicom_3d_bottom.stl")

top_part.union(bottom_part).export("enpicom_3d.stl")

# %%
