from typing import Dict, List
from xmlschema import XMLSchema
from xmlschema.validators import XsdType, XsdComplexType

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
        return getattr(self._schema, name)

    def iter_type_tree(self, xsd_type: XsdType = None):
        yield from self._type_children.get(xsd_type, [])

    def iter_type_roots(self) -> List[XsdType]:
        yield from self._type_children.get(None)



if __name__ == "__main__":
    schex: SchemaEx = SchemaEx('schemas/2.2_ler.xsd')
    for k,v in schex._type_children.items():
        keystr = k.prefixed_name if k is not None else 'None'
        valname = ','.join([v.prefixed_name for v in v])
        print(f"{keystr:<40}: {valname}")
