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
        diameter=c.staff_middle_diameter - c.wall_thickness * 2 - 0.2,
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

insert_base = insert_base.cut(outer).edges(">Z").fillet(5)

insert_foot = (
    insert_base.faces("<Z").extrude(-20).cut(insert_base).edges("<X").chamfer(8)
)

ov.show(insert_base, insert_foot, colors=["darkgreen", "darkblue"])

# %%

insert_base = insert_base.union(
    insert_foot.faces("<X")
    .wires()
    .toPending()
    .transformed(rotate=(0, 90, 0))
    .extrude(-150)
    .edges("<X")
    .fillet(5)
)

ov.show(insert_base)

# %%


insert_base.export("print_files/staff_foot_insert.stl")

# %%
