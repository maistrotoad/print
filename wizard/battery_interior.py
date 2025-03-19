# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 2

shield_width = 29.5
shield_board_height = 99.2
shield_height = 106
shield_thickness = 20
shield_board_thickness = 1.6
shield_spacing = 5

arduino_width = 55
arduino_board_height = 68.5
arduino_height = 75
arduino_thickness = 40

staff_diameter = 80

housing_height = 220

starter_height = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2

cap_width = shield_width + wall_thickness * 2

shield_cap_top = (
    cq.Workplane("XY")
    .rect(
        cap_width,
        wall_thickness,
    )
    .extrude(wall_thickness * 2)
)

click_corner_width = wall_thickness * 2 + shield_board_thickness + tolerance

click_corner = (
    cq.Workplane("XY")
    .rect(
        wall_thickness * 2,
        click_corner_width,
        centered=False,
    )
    .extrude(wall_thickness * 4)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .move(xDist=-tolerance, yDist=-0.5 * (shield_board_thickness + tolerance))
    .rect(
        wall_thickness + tolerance,
        shield_board_thickness + tolerance,
        centered=False,
    )
    .cutBlind(-wall_thickness * 3)
    .translate((-cap_width * 0.5, 0.5 * wall_thickness, -wall_thickness * 2))
)


shield_cap_top = shield_cap_top.union(click_corner).union(
    click_corner.mirror("ZY")
)

ov.show(shield_cap_top)

# %%

click_middle_width = 5
click_middle_height = 20

click_middle_distance = 35

click_middle = (
    cq.Workplane("XY")
    .rect(
        click_middle_width,
        wall_thickness * 2 + shield_board_thickness + tolerance,
        centered=False,
    )
    .extrude(click_middle_height)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .move(
        xDist=-click_middle_width / 2,
        yDist=-0.5 * (shield_board_thickness + tolerance),
    )
    .rect(
        click_middle_width,
        shield_board_thickness + tolerance,
        centered=False,
    )
    .cutBlind(-click_middle_height + wall_thickness)
    .translate((-cap_width * 0.5 - 3.75, 0.5 * wall_thickness, 0))
)

ov.show(click_middle)

# %%

double_click_bottom = click_corner.union(click_corner.mirror("ZY"))


arduino_and_battery_bottom = (
    cq.Workplane("XY")
    .rect(
        cap_width + 7.5,
        wall_thickness,
    )
    .extrude(wall_thickness * 2)
    .union(double_click_bottom)
)


arduino_and_battery_bottom = arduino_and_battery_bottom.rotate(
    (0, 0, 0), (1, 0, 0), 180
).translate((0, 0, wall_thickness * 2))


arduino_and_battery_bottom = arduino_and_battery_bottom.union(
    click_middle
).union(click_middle.translate((click_middle_distance, 0, 0)))

y_offset = 15

arduino_and_battery_bottom = arduino_and_battery_bottom.translate(
    (0, -y_offset, 0)
)

plate_outer_diameter = staff_diameter - wall_thickness * 2 - tolerance * 2


base_plate_adruino = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=plate_outer_diameter,
    )
    .extrude(wall_thickness)
)

arduino_and_battery_bottom = arduino_and_battery_bottom.union(
    base_plate_adruino
)

ov.show(arduino_and_battery_bottom)

# %%


arduino_top_thickness = 3.4
arduino_top_click_width = 19.3
arduino_top_click_height = 11

arduino_and_battery_top = (
    cq.Workplane("XY")
    .workplane(offset=arduino_board_height + wall_thickness)
    .rect(arduino_top_click_width, arduino_top_thickness + wall_thickness * 2)
    .extrude(-arduino_top_click_height)
    .rect(arduino_top_click_width, arduino_top_thickness)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .rect(arduino_top_click_width, arduino_top_thickness + wall_thickness * 2)
    .extrude(shield_board_height - arduino_board_height + wall_thickness)
    .translate((3, 4.7, 0))
    .union(
        double_click_bottom.translate(
            (0, -click_corner_width - wall_thickness, shield_board_height)
        )
    )
    .faces(">Z")
    .extrude(30)
)

total_height = shield_height + 26


top_plate = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=13,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=plate_outer_diameter,
    )
    .extrude(wall_thickness)
)

arduino_and_battery_top = arduino_and_battery_top.translate((0, -y_offset, 0))

arduino_and_battery_top = (
    arduino_and_battery_top.union(top_plate)
    .faces(">Z[-2]")
    .rect(45, 45, forConstruction=True)
    .vertices()
    .circle(3.5)
    .extrude(-total_height + wall_thickness - tolerance * 2)
    .faces("<Z")
    .workplane()
    .rect(45, 45, forConstruction=True)
    .vertices()
    .circle(1.25)
    .cutBlind(-wall_thickness * 3)
)

arduino_and_battery_bottom = (
    arduino_and_battery_bottom.faces("<Z")
    .rect(45, 45, forConstruction=True)
    .vertices()
    .circle(3.5)
    .cutBlind(tolerance * 2)
    .faces("<Z[-2]")
    .workplane()
    .rect(45, 45, forConstruction=True)
    .vertices()
    .circle(1.25)
    .cutThruAll()
)


ov.show(
    arduino_and_battery_bottom,
    arduino_and_battery_top,
    colors=["darkgreen", "darkblue"],
)

# %%

arduino_and_battery_bottom.export("arduino_and_battery_bottom.stl")
arduino_and_battery_top.export("arduino_and_battery_top.stl")

# %%

base_plate_inner_diameter = shield_width + shield_thickness - tolerance * 2


base_plate = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=base_plate_inner_diameter,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=plate_outer_diameter,
    )
    .extrude(wall_thickness)
)


shield_cap_top = shield_cap_top.union(
    shield_cap_top.rotate((0, 0, 0), (0, 0, 1), 90).translate(
        (0, -0.5 * shield_width - wall_thickness * 0.5 + -tolerance, 0)
    )
)


shield_cap_top = shield_cap_top.union(
    shield_cap_top.rotate((0, 0, 0), (0, 0, 1), 180).translate(
        (
            cap_width * 0.5 - wall_thickness * 0.5 + tolerance,
            -(shield_width + wall_thickness) * 0.5,
            0,
        )
    )
).translate(
    (
        -(shield_width + wall_thickness) * 0.25 - tolerance * 0.5,
        (shield_width + wall_thickness) * 0.25,
        -wall_thickness,
    )
)

shield_cap_top = shield_cap_top.union(base_plate)

ov.show(shield_cap_top)

# %%

shield_cap_bottom = shield_cap_top.mirror("XY").translate(
    (0, 0, -shield_board_height)
)

ov.show(shield_cap_bottom)

# %%

shield_cap_bottom = (
    shield_cap_bottom.faces(">Z[1]")
    .workplane()
    .transformed(rotate=(0, 0, 33))
    .rect(
        base_plate_inner_diameter - 5,
        base_plate_inner_diameter - 5,
        forConstruction=True,
    )
    .vertices()
    .circle(3.5)
    .extrude(shield_board_height + tolerance)
)

shield_cap_top = (
    shield_cap_top.faces(">Z")
    .transformed(rotate=(0, 0, 33), offset=(0, 0, wall_thickness))
    .rect(
        base_plate_inner_diameter - 5,
        base_plate_inner_diameter - 5,
        forConstruction=True,
    )
    .vertices()
    .cboreHole(2.5, 6, 0.5)
    .cut(shield_cap_bottom)
)

ov.show(
    shield_cap_top,
    shield_cap_bottom,
    colors=["darkgreen", "darkBlue"],
    alphas=[1, 0.8],
)

# %%
shield_cap_top.export("shield_cap_top.stl")
shield_cap_bottom.export("shield_cap_bottom.stl")

# %%
