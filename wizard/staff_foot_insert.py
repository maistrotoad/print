# %%

import cadquery as cq
import const as c
import ocp_vscode as ov

diameter = c.staff_middle_diameter + 30

engraved_column = (
    cq.Workplane("XY")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .extrude(c.column_height - c.slope_height * 2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .workplane(offset=c.slope_height * 0.8)
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .loft(ruled=True)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=diameter,
    )
    .extrude(c.slope_height * 0.2)
    .faces(">Z")
    .polygon(
        nSides=8,
        circumscribed=True,
        diameter=c.staff_middle_diameter - c.wall_thickness * 2 - 0.65,
    )
    .cutThruAll()
)

ov.show(engraved_column)


# %%

sub_bottom_outer = cq.Workplane(
    obj=(
        engraved_column.split(keepBottom=True)
        .translate((0, 77, 0))
        .val()
        .scale(0.65)
    )
)

sub_bottom_inner = cq.Workplane(
    obj=(
        engraved_column.split(keepBottom=True)
        .translate((0, 58, 0))
        .val()
        .scale(0.65)
    )
)

outer = sub_bottom_outer.union(sub_bottom_inner)


ov.show(outer)


# %%

insert_base = cq.Workplane("XY").rect(32, 22).extrude(60).translate((0, 44, 0))

ov.show(insert_base, outer, colors=["darkgreen"])

# %%

insert_base = insert_base.cut(outer)

insert_foot = insert_base.faces("<Z").extrude(-20).cut(insert_base)

ov.show(
    insert_base,
    insert_foot,
    insert_foot.faces("<Y"),
    colors=["darkgreen", "darkblue"],
)


# %%

insert_foot = (
    insert_foot.faces("<Y")
    .wires()
    .toPending()
    .transformed(rotate=(90, 0, 0), offset=(0, 0, -17.5))
    .workplane(offset=-200)
    .rect(12, 5)
    .loft(combine=True)
    .edges(">>Z[5]")
    .fillet(6)
)

ov.show(insert_foot, colors=["darkgreen"])

# %%

insert_base = insert_base.edges(">Z").fillet(8).union(insert_foot)

ov.show(insert_base)

# %%


insert_base.export("print_files/staff_foot_insert.stl")

# %%
