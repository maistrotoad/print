# %%

import cadquery as cq
import ocp_vscode as ov

size = 21

sphere_radius = 2
rod_radius = 0.8

hexagon_middle = cq.Workplane("XY").polygon(6, size)

height = (
    hexagon_middle.vertices("<(1,1,0)")
    .val()
    .distance(hexagon_middle.vertices("<(1,-1,0)").val())
)

triangle_top = cq.Workplane("XY").workplane(offset=height / 2).polygon(3, 13)

triangle_bottom = (
    cq.Workplane("XY").workplane(offset=-height / 2).polygon(3, 13)
)


def get_vector(value: cq.Workplane):
    return value.workplane(centerOption="CenterOfMass").val()


def get_rod(point_a: cq.Workplane, point_b: cq.Workplane):
    plane_a = cq.Plane(
        origin=get_vector(point_a),
        normal=get_vector(point_a) - get_vector(point_b),
    )

    rod = (
        cq.Workplane(plane_a)
        .circle(rod_radius)
        .workplane(offset=-point_a.val().distance(point_b.val()))
        .circle(rod_radius)
        .loft()
    )
    return rod


# %%

rods_top = [
    get_rod(
        triangle_top.vertices("<X and <Y"), triangle_top.vertices("<X and >Y")
    ),
    get_rod(triangle_top.vertices("<X and <Y"), triangle_top.vertices(">X")),
    get_rod(triangle_top.vertices("<X and >Y"), triangle_top.vertices(">X")),
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

ov.show(
    hexagon_middle,
    triangle_top,
    triangle_bottom,
    *rods_top,
    *rods_hexagon,
    *rods_bottom,
)

# %%


enpicom_3d = triangle_top.union(hexagon_middle).union(triangle_bottom)

for r in [*rods_top, *rods_hexagon, *rods_bottom]:
    enpicom_3d = enpicom_3d.union(r)


ov.show(enpicom_3d)

enpicom_3d.export("enpicom_3d.stl")

# %%
