from tabulate import tabulate
from rich.console import Console
from rich.table import Table
from rich import box
from xmlschema.validators import XsdElement

from wrapper import SchemaEx


if __name__ == "__main__":
    schex: SchemaEx = SchemaEx('schemas/2.2_ler.xsd')

    console = Console()

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.SIMPLE,
        show_lines=True,
    )

    table.add_column("Type", width=40, no_wrap=True, style="bold yellow")
    table.add_column("Children", width=80, overflow="fold")

    for k, values in schex._type_hierarchy.items():
        key = k.prefixed_name if k is not None else "None"
        val = ", ".join(v.prefixed_name for v in values)

        table.add_row(key, val)

    for type in schex._type_hierarchy.items():
        key = k.prefixed_name if k is not None else "None"
        val = ", ".join(v.prefixed_name for v in values)

        table.add_row(key, val)

    console.print(table)

    print()
    print('### Root types: ###')

    for roottype in schex.iter_type_roots():
        print("  -", roottype.prefixed_name)

    print()
    print('### Root types, with their children: ###')
    for roottype in schex.iter_type_roots():
        print("  -", roottype.prefixed_name)
        for child in schex._type_hierarchy[roottype]:
            print("    -", child.prefixed_name)

    print()
    print('### Root types, with their trees: ###')

    for roottype in schex.iter_type_roots():
        print("  -", roottype.prefixed_name)
        for depth, child in schex.walk_type_hierarchy(roottype):
            if depth == 0:
                continue
            print("    " * depth + "- " + child.prefixed_name)

    print()
    print('### absgmltype ###')
    absgmltype = schex.maps.types['{http://www.opengis.net/gml/3.2}AbstractGMLType']

    for x in schex.walk_type_hierarchy(absgmltype):
        print(x[1].prefixed_name)

    print()
    print('### schex.elements.values ###')

    for elm in schex.elements.values():
        print(elm.prefixed_name)
        for subelm in elm.iter():
            assert isinstance(subelm, XsdElement), "Expected XsdType, got: " + repr(subelm)
            print('  -', subelm.name)
