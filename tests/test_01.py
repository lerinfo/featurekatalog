from wrapper import SchemaEx

schex = SchemaEx('schemas/2.2_ler.xsd')

def test_01():
    l = schex.elements.items()
    assert len(l) == 26

