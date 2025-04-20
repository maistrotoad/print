# %%

import cadquery as cq
import const as c
import ocp_vscode as ov

battery_in_case = (
    cq.Workplane("YZ")
    .rect(c.shield_width, c.shield_board_height)
    .extrude(c.shield_board_thickness)
    .faces(">X")
    .rect(c.shield_width - 6, c.shield_board_height - 6)
    .extrude(c.shield_with_battery_thickness - c.shield_board_thickness)
    .edges(">X")
    .fillet(5)
    .faces(">Z[-2]")
    .workplane()
    .move(xDist=10)
    .rect(12, 20)
    .extrude(3 + c.shield_with_usb_height - c.shield_board_height)
    .translate((1, 0, c.shield_board_height * 0.5 + c.wall_thickness))
)

ov.show(battery_in_case)

# %%

battery_mount_inner_diameter = c.staff_middle_diameter - 2 * c.wall_thickness

battery_mount = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=battery_mount_inner_diameter,
    )
    .extrude(c.wall_thickness)
    .faces(">Z")
    .rect(c.wall_thickness, c.shield_width)
    .extrude(c.shield_board_height + c.wall_thickness)
    .faces(">X[-2]")
    .workplane()
    .move(yDist=c.shield_board_height * 0.5 + c.wall_thickness)
    .rect(c.shield_width - 4, c.shield_board_height - 4, forConstruction=True)
    .vertices()
    .circle(1.5)
    .cutThruAll()
    .faces("<Z")
    .workplane()
    .move(yDist=c.shield_width * 0.5, xDist=-30)
    .rect(60, 10, centered=False)
    .cutThruAll()
    .faces("<Z")
    .workplane()
    .move(yDist=-c.shield_width * 0.5, xDist=-30)
    .rect(60, -10, centered=False)
    .cutThruAll()
)

dual_battery = battery_in_case.union(
    battery_in_case.rotate((0, 0, 0), (0, 0, 1), 180)
)

ov.show(
    battery_mount,
    dual_battery,
    colors=["darkgreen", "darkblue"],
)

# %%


engraved_column = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .extrude(
        c.shield_with_usb_height - c.slope_height * 2 + 2 * c.wall_thickness
    )
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter + c.buldge_diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter - c.wall_thickness * 2,
    )
    .cutThruAll()
)

ov.show(
    engraved_column,
    battery_mount,
    dual_battery,
    colors=["darkgreen", "darkblue"],
    alphas=[0.7, 1],
)

# %%

plate_cut = (
    cq.Workplane("XY")
    .move(yDist=-50, xDist=battery_mount_inner_diameter * 0.5 - 2)
    .rect(100, 100, centered=False)
    .extrude(200)
    .union(
        cq.Workplane("XY")
        .move(yDist=-50, xDist=-battery_mount_inner_diameter * 0.5 + 2)
        .rect(-100, 100, centered=False)
        .extrude(200)
    )
)

ov.show(
    engraved_column.cut(plate_cut).union(battery_mount),
    engraved_column.intersect(plate_cut),
    dual_battery,
    colors=["darkgreen", "darkblue"],
    alphas=[0.7, 0.7, 1],
)

# %%


battery_case_assembly = engraved_column.cut(plate_cut).union(battery_mount)

battery_case_assembly.export("print_files/battery_case_assembly.stl")

# %%
