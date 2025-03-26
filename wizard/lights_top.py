# %%

import cadquery as cq
import ocp_vscode as ov

wall_thickness = 10

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

staff_middle_diameter = 50

slope_height = 5
buldge_diameter = 10

tolerance = 0.2
casing_height = 200

casing_start_inner_diameter = 70

strip_width = 12.5
global_cut_depth = -6
mask_depth = -4 + tolerance

crystal_middle_diameter = 144
crystal_base_height = 34
crystal_middle_height = 55
crystal_top_height = 34

crystal_total_height = (
    crystal_base_height
    + crystal_middle_height
    + crystal_top_height
    + slope_height
    + 2
)

# %%

crystal_bottom_cap = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter,
    )
    .extrude(slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .extrude(2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - wall_thickness * 2,
    )
    .cutBlind(-slope_height - 2)
)

ov.show(crystal_bottom_cap)


# %%

crystal_top_cap = (
    cq.Workplane("XY")
    .workplane(
        offset=crystal_base_height
        + crystal_middle_height
        + crystal_top_height
        + 6
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - 4,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .extrude(2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .workplane(offset=slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter + buldge_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .extrude(1)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - 4,
    )
    .cutBlind(-slope_height)
)

ov.show(crystal_bottom_cap, crystal_top_cap)

# %%

crystal = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - wall_thickness * 2,
    )
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .extrude(slope_height + 2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .workplane(offset=crystal_base_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=crystal_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .extrude(crystal_middle_height)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=crystal_middle_diameter,
    )
    .workplane(offset=crystal_top_height)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .extrude(2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=staff_middle_diameter - 4,
    )
    .cutBlind(-10)
    .cut(
        cq.Workplane("XY")
        .workplane(offset=wall_thickness + 4)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=staff_middle_diameter - 12,
        )
        .workplane(offset=crystal_base_height)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=crystal_middle_diameter - wall_thickness * 2 - 8,
        )
        .loft(ruled=True)
        .faces(">Z")
        .extrude(crystal_middle_height - wall_thickness)
        .faces(">Z")
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=crystal_middle_diameter - wall_thickness * 2 - 8,
        )
        .workplane(offset=crystal_top_height - 8)
        .polygon(
            nSides=8,
            circumscribed=True,
            diameter=2,
        )
        .loft(ruled=True)
    )
)

ov.show(
    crystal_bottom_cap,
    crystal_top_cap,
    crystal,
    colors=["darkgreen", "darkgreen", "darkblue"],
    alphas=[1, 1, 0.8],
)

# %%

helix_bottom_height = crystal_base_height + crystal_middle_height * 0.5

helix_bottom_radius = staff_middle_diameter * 0.5  # Radius of the helix
p = helix_bottom_height * 8  # Pitch of the helix

# Helix
helix_bottom_wire = cq.Wire.makeHelix(
    pitch=p,
    height=helix_bottom_height,
    radius=helix_bottom_radius,
    center=(0, crystal_middle_diameter * 0.5, 0),
)
helix = cq.Workplane("XY").spline(
    [
        (staff_middle_diameter * 0.5 - 6, 0, 0),
        (staff_middle_diameter * 0.5 - 6, 0, slope_height * 2),
        (crystal_middle_diameter * 0.5 - 12, 0, crystal_base_height + 8),
        (
            crystal_middle_diameter * 0.5 - 6,
            0,
            (crystal_base_height + crystal_base_height + crystal_middle_height)
            * 0.5
            + 2,
        ),
        (
            crystal_middle_diameter * 0.5 - 12,
            0,
            crystal_base_height + crystal_middle_height + 2,
        ),
        (staff_middle_diameter * 0.5 - 14, 0, crystal_total_height),
        (
            staff_middle_diameter * 0.5 - 20,
            0,
            crystal_total_height + slope_height,
        ),
        (
            staff_middle_diameter * 0.5 - 24,
            0,
            crystal_total_height + slope_height + 2,
        ),
    ],
)

ov.show(crystal, helix)

# %%
mid_x = 0.5 * strip_width


helix_cut = (
    cq.Workplane("XY")
    .transformed(
        rotate=(0, 0, -90),
        offset=(staff_middle_diameter * 0.5 - 6, strip_width * 0.5, 0),
    )
    .sketch()
    .segment((0, 0), (strip_width, 0))
    .segment((strip_width, 4))
    .segment((mid_x + strip_width * 0.1, 4))
    .segment((mid_x + strip_width * 0.1, 6))
    .segment((mid_x + strip_width * 0.3, 6))
    .segment((mid_x + strip_width * 0.3, 18))
    .segment((mid_x - strip_width * 0.3, 18))
    .segment((mid_x - strip_width * 0.3, 6))
    .segment((mid_x - strip_width * 0.1, 6))
    .segment((mid_x - strip_width * 0.1, 4))
    .segment((0, 4))
    .close()
    .assemble(tag="face")
    .edges("%LINE", tag="face")
    .vertices()
    .fillet(1)
    .finalize()
    .sweep(helix, isFrenet=False)
)

ov.show(
    crystal.union(crystal_bottom_cap).union(crystal_top_cap),
    helix_cut,
    helix,
    colors=["darkgreen"],
    alphas=[0.8],
)

# %%

box_height = crystal_base_height + crystal_middle_height + crystal_top_height

helix_mask_to_intersect = (
    (
        cq.Workplane("XY")
        .workplane(offset=slope_height + box_height * 0.5 + 1.5)
        .box(
            crystal_middle_diameter * 2,
            crystal_middle_diameter * 2,
            box_height,
        )
    )
    .union(crystal_top_cap)
    .union(crystal_bottom_cap)
)

ov.show(helix_mask_to_intersect)

# %%

helix_mask = (
    cq.Workplane("XY")
    .transformed(
        rotate=(0, 0, -90),
        offset=(
            staff_middle_diameter * 0.5 - 6 - tolerance,
            strip_width * 0.5,
            0,
        ),
    )
    .sketch()
    .segment(
        (mid_x + strip_width * 0.3 - tolerance, 18),
        (mid_x - strip_width * 0.3 + tolerance, 18),
    )
    .segment((mid_x - strip_width * 0.3 + tolerance, 6 - tolerance))
    .segment((mid_x - strip_width * 0.1 + tolerance, 6 - tolerance))
    .segment((mid_x - strip_width * 0.1 + tolerance, 4 + tolerance))
    .segment((mid_x + strip_width * 0.1 - tolerance, 4 + tolerance))
    .segment((mid_x + strip_width * 0.1 - tolerance, 6 - tolerance))
    .segment((mid_x + strip_width * 0.3 - tolerance, 6 - tolerance))
    .close()
    .assemble(tag="face_mask")
    .edges("%LINE", tag="face_mask")
    .vertices()
    .fillet(1)
    .finalize()
    .sweep(helix, isFrenet=False)
    .intersect(helix_mask_to_intersect)
)

ov.show(helix_mask)

# %%

helix_cut = helix_cut.union(helix_cut.mirror("ZY"))
helix_cut = helix_cut.union(helix_cut.rotate((0, 0, 0), (0, 0, 1), 90))


ov.show(helix_cut, helix_mask, colors=["darkgreen", "darkblue"], alphas=[0.5])

# %%


crystal = (
    crystal.union(crystal_bottom_cap).union(crystal_top_cap).cut(helix_cut)
)

ov.show(crystal, helix_mask, colors=["darkgreen", "darkblue"], alphas=[1])

# %%

crystal.export("print_files/crystal.stl")
helix_mask.export("print_files/crystal_mask.stl")

# %%
