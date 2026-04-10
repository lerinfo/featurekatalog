from typing import Dict, List
from collections.abc import Iterator

import tabulate
from xmlschema import XMLSchema
from xmlschema.validators import XsdType, XsdComplexType
from tabulate import tabulate

from rich.console import Console
from rich.table import Table
from rich import box


class SchemaEx:
    _type_children: Dict[XsdType|None, List[XsdType]] = None
    #_type_children[None] holds all the root types, i.e. those without a base type.
    def _init_type_children_for_type(self, elmtype: XsdType):
        if not isinstance(elmtype, XsdType):
            raise TypeError("Expected XsdType, got: " + repr(elmtype))
        parenttype = getattr(elmtype, "base_type", None)
        if not parenttype in self._type_children:
            self._type_children[parenttype] = []
        if not elmtype in self._type_children[parenttype]:
            self._type_children[parenttype].append(elmtype)
        if parenttype is not None:
            self._init_type_children_for_type(parenttype)

    def _init_type_children(self):
        self._type_children = {}
        self._type_children[None] = []
        for elm in self.schema.elements.values():
            elmtype = elm.type
            self._init_type_children_for_type(elmtype)
    
    def __init__(self, xsd_or_schema, *args, **kwargs):
        if isinstance(xsd_or_schema, XMLSchema):
            self.schema = xsd_or_schema
        else:
            self.schema = XMLSchema(xsd_or_schema, *args, **kwargs)
        self._init_type_children()

    def __getattr__(self, name):
        return getattr(self.schema, name)

    def iter_type_tree(self, xsd_type: XsdType, depth: int = 0) -> Iterator[tuple[int, XsdType]]:
        '''
        yields (depth, xsd_type) for xsd_type and all its children, recursively.
        '''
        yield (depth, xsd_type)
        for child in self._type_children.get(xsd_type, []):
            yield from self.iter_type_tree(child, depth + 1)

    def iter_type_roots(self) -> Iterator[XsdType]:
        yield from self._type_children.get(None)


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

    for k, values in schex._type_children.items():
        key = k.prefixed_name if k is not None else "None"
        val = ", ".join(v.prefixed_name for v in values)

        table.add_row(key, val)

    for type in schex._type_children.items():
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
        for child in schex._type_children[roottype]:
            print("    -", child.prefixed_name)

    print()
    print('### Root types, with their trees: ###')

    for roottype in schex.iter_type_roots():
        print("  -", roottype.prefixed_name)
        for depth, child in schex.iter_type_tree(roottype):
            if depth == 0:
                continue
            print("    " * depth + "- " + child.prefixed_name)
