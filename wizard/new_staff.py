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

tolerance = 0.1

battery_housing = (
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

ov.show(battery_housing, colors=["grey"], alphas=[1])
# %%

battery_housing = (
    battery_housing.faces(">Z")
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
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.4)
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
    .cutBlind(-slope_height * 2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 2,
    )
    .polygon(nSides=8, circumscribed=True, diameter=staff_diameter)
    .extrude(starter_height - slope_height)
)

ring_cap = (
    cq.Workplane("XY")
    .workplane(offset=starter_height - slope_height - wall_thickness * 0.5)
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
    .extrude(slope_height * 2)
)

extension = battery_housing.split(keepTop=True)
battery_housing = battery_housing.split(keepBottom=True)

ov.show(
    battery_housing,
    extension,
    ring_cap,
    ring_cap.faces("<X"),
    colors=["grey", "darkblue"],
    alphas=[1, 1, 0.75],
)


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
        diameter=staff_diameter - wall_thickness * 2 - 0.5,
    )
    .extrude(wall_thickness)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_diameter - wall_thickness * 4 - 0.5,
    )
    .extrude(-40 + wall_thickness)
)

spring_insert = spring_insert.union(spring)

ov.show(
    spring_insert,
    battery_housing,
    colors=["darkblue", "grey"],
    alphas=[1, 0.95],
)

# %%
