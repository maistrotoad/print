import cadquery as cq
import const as c


def get_battery_in_case() -> cq.Workplane:
    return (
        cq.Workplane("YZ")
        .rect(c.shield_width, c.shield_board_height)
        .extrude(c.shield_board_thickness)
        .faces(">X")
        .workplane()
        .move(yDist=3)
        .rect(c.shield_width - 6, c.shield_board_height - 6)
        .extrude(c.shield_with_battery_thickness - c.shield_board_thickness)
        .edges(">X")
        .fillet(5)
        .faces(">Z[-1]")
        .workplane()
        .move(xDist=10)
        .rect(12, 20)
        .extrude(3 + c.shield_with_usb_height - c.shield_board_height)
    )


def get_dual_battery():
    return (
        get_battery_in_case()
        .translate((1.5, 0, 0))
        .union(
            get_battery_in_case()
            .rotate((0, 0, 0), (0, 0, 1), 180)
            .translate((-1.5, 0, 0))
        )
    )
