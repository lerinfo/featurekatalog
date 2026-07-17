from typing import Dict, List
from collections.abc import Iterator

from xmlschema.validators import XsdType, XsdComplexType, XsdGroup, XsdElement
from xmlschema import XMLSchema


class SchemaEx:
    '''
    A wrapper around xmlschema.Schema. Called SchemaEx to indicate its an extension.
    It makes it easy to iterate/traverse the types in a schema.
    '''
    _type_hierarchy: Dict[XsdType|None, List[XsdType]] = {}
    """
    Mapping of base types to their derived types.
    Used for top-down traversal of the type inheritance hierarchy.
    """
    def _register_type_and_ancestors(self, elmtype: XsdType):
        """
        Register ``elmtype`` under its base type in ``_type_hierarchy`` and
        recursively register its ancestor types.

        The ``None`` entry holds root types, i.e. types without a base type.
        """
        if not isinstance(elmtype, XsdType):
            raise TypeError("Expected XsdType, got: " + repr(elmtype))
        parenttype = getattr(elmtype, "base_type", None)
        if not parenttype in self._type_hierarchy:
            self._type_hierarchy[parenttype] = []
        if not elmtype in self._type_hierarchy[parenttype]:
            self._type_hierarchy[parenttype].append(elmtype)
        if parenttype is not None:
            self._register_type_and_ancestors(parenttype)

    def _init_type_hierarchy(self):
        '''
        Called by constructor only.
        '''
        if len(self._type_hierarchy) != 0:
            return
        self._type_hierarchy = {}
        self._type_hierarchy[None] = []
        for elm in self.schema.elements.values():
            elmtype = elm.type
            self._register_type_and_ancestors(elmtype)
    
    def __init__(self, xsd_or_schema, *args, **kwargs):
        if isinstance(xsd_or_schema, XMLSchema):
            self.schema = xsd_or_schema
        else:
            self.schema = XMLSchema(xsd_or_schema, *args, **kwargs)
        self._init_type_hierarchy()

    def __getattr__(self, name):
        return getattr(self.schema, name)

    def walk_type_hierarchy(self, xsd_type: XsdType, depth: int = 0) -> Iterator[tuple[int, XsdType]]:
        '''
        Yield (depth, xsd_type) for the given type and recursively for its child types.
        '''
        yield (depth, xsd_type)
        for child in self._type_hierarchy.get(xsd_type, []):
            yield from self.walk_type_hierarchy(child, depth + 1)

    def iter_type_roots(self) -> Iterator[XsdType]:
        '''
        Returns all the XsdTypes that don't inherit anything, ie base_type = None
        '''
        yield from self._type_hierarchy.get(None)

    def iter_type_ancestors(self, xsd_type: XsdType) -> Iterator[XsdType]:
        parent = getattr(xsd_type, "base_type", None)
        while parent is not None:
            yield parent
            parent = getattr(parent, "base_type", None)
