import math

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
staff_middle_diameter = 50

casing_start_inner_diameter = 70
casing_height = 75


housing_height = 220
column_height = 200


def get_face_width(d):
    return d * math.tan(math.pi / 8)


face_width = get_face_width(staff_middle_diameter)

starter_height = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2

faces = list(
    reversed(
        [
            ">X",
            ">(1,-1,0)",
            "<Y",
            ">(-1,-1,0)",
            "<X",
            ">(-1,1,0)",
            ">Y",
            ">(1,1,0)",
        ]
    )
)
