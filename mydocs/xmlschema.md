Der er i alt 234 top level klasser i xmlschema. De fleste ligger i xmlschema/validators, med 104 klasser. Se alle klasser i filen xmlschema_class_tree.txt.

Jeg har valgt kun at opremse nogle få, som har relevans for mig:

XsdValidator
  XMLSchemaBase
    XMLSchema10
      ObservedXMLSchema10
    XMLSchema11
      ObservedXMLSchema11
  XsdComponent
    XsdAlternative
    XsdAnnotation
    XsdAssert
    XsdAttribute
      Xsd11Attribute
    XsdAttributeGroup
    XsdElement
      Xsd11Element
    XsdGroup
      Xsd11Group
    XsdType
      XsdComplexType
        Xsd11ComplexType
      XsdSimpleType
        XsdAtomic
          XsdAtomicBuiltin
          XsdAtomicRestriction
            Xsd11AtomicRestriction
        XsdList
        XsdUnion
          Xsd11Union

Så... utroligt mange ting, inkl XsdComponent, er altså subclass af XsdValidator.

Når jeg kigger i deres API (https://xmlschema.readthedocs.io/en/latest/api.html), så kan jeg ikke finde nogen entry for XsdValidator. Jeg gætter på, at de af en eller anden grund ikke genererer api docs på den.

## XsdType

https://github.com/sissaschool/xmlschema/blob/64b103f211f292b6e076c404dfa83e2239b1341e/xmlschema/validators/xsdbase.py#L710-L898

    base_type: Optional[BaseXsdType] = None
    derivation: Optional[str] = None
    _final: Optional[str] = None
    ref: Optional[BaseXsdType]
