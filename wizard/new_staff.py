# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 2

shield_width = 29.5
shield_height = 106
shield_thickness = 20
shield_board_thickness = 1.6
shield_spacing = 5

arduino_width = 55
arduino_height = 75
arduino_thickness = 40

staff_diameter = 80

housing_height = 220

starter_height = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2

# %%

battery_housing_spring_chamber = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 4,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .extrude(wall_thickness)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .extrude(starter_height - wall_thickness - slope_height)
)

ov.show(battery_housing_spring_chamber)

# %%


def tag_wall(wp, face, pos, direction=1):
    wp = (
        wp.faces(f"{face}[{pos}]")
        .workplane(centerOption="CenterOfMass")
        .tag("x_n")
        .move(yDist=(-starter_height * 0.2) * direction)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=16,
        )
        .cutBlind(-tolerance * 2, taper=75)
        .workplaneFromTagged("x_n")
        .move(yDist=(starter_height * 0.1) * direction)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=8,
        )
        .cutBlind(-tolerance * 2, taper=75)
        .workplaneFromTagged("x_n")
        .move(yDist=(starter_height * 0.3) * direction)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=4,
        )
        .cutBlind(-tolerance * 2, taper=75)
    )
    return wp


faces = [
    ">X",
    ">(1,-1,0)",
    "<Y",
    ">(-1,-1,0)",
    "<X",
    ">(-1,1,0)",
    ">Y",
    ">(1,1,0)",
]


def tag_all_walls(wp, pos):
    direction = 1

    for f in faces:
        wp = tag_wall(wp, face=f, pos=pos, direction=direction)
        direction *= -1

    return wp


battery_housing_spring_chamber = tag_all_walls(
    battery_housing_spring_chamber, pos=-1
)

ov.show(
    battery_housing_spring_chamber,
    colors=["grey"],
    alphas=[1],
)
# %%

ring_cut = (
    battery_housing_spring_chamber.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .tag("slope_start")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + tolerance * 2,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + tolerance * 2,
    )
    .extrude(slope_height * 0.4)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + tolerance * 2,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .loft(ruled=True)
)

battery_housing_spring_chamber = (
    battery_housing_spring_chamber.workplaneFromTagged("slope_start")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8, circumscribed=True, diameter=staff_diameter + buldge_diameter
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height * 2)
)

ring_cap = (
    cq.Workplane("XY")
    .workplane(offset=starter_height - slope_height - wall_thickness)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + tolerance * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter + wall_thickness * 2,
    )
    .extrude(slope_height * 2 + wall_thickness)
    .cut(ring_cut)
)

ov.show(
    battery_housing_spring_chamber,
    ring_cap,
    colors=["grey", "darkblue"],
    alphas=[1, 1, 0.75],
)


# %%


def add_knob_mount(wp, face):
    wp = (
        wp.faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(slope_height)
        .extrude(wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .circle(slope_height * 1.5)
        .extrude(wall_thickness)
        .faces(face)
        .workplane(centerOption="CenterOfMass")
        .tag("mount_face")
        .move(xDist=-slope_height * 1.5, yDist=slope_height)
        .rect(slope_height * 3, slope_height * 3, centered=False)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-slope_height * 1.5, yDist=-slope_height)
        .rect(slope_height * 3, -slope_height * 3, centered=False)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=slope_height * 1.5)
        .circle(wall_thickness * 0.5)
        .cutBlind(-wall_thickness)
        .faces(face)
        .workplaneFromTagged("mount_face")
        .move(xDist=-slope_height * 1.5)
        .circle(wall_thickness * 0.5)
        .cutBlind(-wall_thickness)
    )
    return wp


ring_cap = add_knob_mount(ring_cap, "<X")
ring_cap = add_knob_mount(ring_cap, ">X")


ring_knob = (
    cq.Workplane(
        "YZ",
        origin=ring_cap.faces("<X")
        .workplane(centerOption="CenterOfMass")
        .val(),
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=slope_height * 1.5 + wall_thickness * 6,
    )
    .extrude(-wall_thickness)
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .tag("knob_face")
    .circle(slope_height * 1.5 + tolerance)
    .circle(slope_height * 1.5 + wall_thickness + tolerance)
    .extrude(wall_thickness + tolerance)
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .circle(slope_height + tolerance * 2)
    .circle(slope_height * 1.5 + wall_thickness + tolerance)
    .extrude(wall_thickness - tolerance * 2)
    .faces(">X")
    .rect(slope_height * 4, slope_height * 2 + tolerance * 2)
    .cutBlind(-wall_thickness * 2 + tolerance * 2)
    .workplaneFromTagged("knob_face")
    .move(yDist=-slope_height * 1.5 - tolerance * 2)
    .circle(wall_thickness * 0.5 - tolerance * 0.5)
    .extrude(wall_thickness)
    .workplaneFromTagged("knob_face")
    .move(yDist=slope_height * 1.5 + tolerance * 2)
    .circle(wall_thickness * 0.5 - tolerance * 0.5)
    .extrude(wall_thickness)
)

ring_cap = ring_cap.cut(
    cq.Workplane("XY")
    .transformed(offset=(-60, -tolerance * 0.5, 0))
    .box(120, 120, 100, centered=False)
)


ov.show(
    battery_housing_spring_chamber,
    ring_cap,
    ring_knob,
    alphas=[1, 0.8, 1],
    colors=["gray", "darkorange"],
)
# %%


battery_housing_start = (
    cq.Workplane(
        "XY",
        origin=battery_housing_spring_chamber.faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .val(),
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height + wall_thickness)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .extrude(starter_height - slope_height)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8, circumscribed=True, diameter=staff_diameter + buldge_diameter
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height * 2)
)

battery_housing_start = tag_all_walls(battery_housing_start, pos=-2)

ov.show(battery_housing_start)

# %%

insert_diameter = staff_diameter - wall_thickness * 4 - 0.5

spring_wire_thickness = 2

r = (insert_diameter / 2) - (spring_wire_thickness * 2)  # Radius of the helix
p = 10  # Pitch of the helix
h = 40  # Height of the helix


# Helix
wire = cq.Wire.makeHelix(pitch=p, height=h, radius=r)
helix = cq.Workplane(obj=wire)
# Final result. A circle sweeped along a helix.
spring = (
    cq.Workplane("XZ")
    .center(r, 0)
    .circle(spring_wire_thickness)
    .sweep(helix, isFrenet=True)
)

spring_insert = (
    cq.Workplane("XY")
    .workplane(offset=4)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2 - tolerance * 2,
    )
    .extrude(wall_thickness)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 4 - tolerance * 2,
    )
    .extrude(-40 + wall_thickness)
)

spring_insert = spring_insert.union(spring)

ov.show(
    spring_insert,
    battery_housing_spring_chamber,
    battery_housing_start,
    ring_cap,
    ring_knob,
    colors=["darkblue", "darkgreen", "brown"],
    alphas=[1, 0.95, 0.95],
)

# %%

spring_insert.export("spring_insert.stl")
battery_housing_spring_chamber.export("battery_housing_spring_chamber.stl")
battery_housing_start.export("battery_housing_start.stl")
ring_cap.export("ring_cap.stl")
ring_knob.export("ring_knob.stl")

# %%
