import pytest
from wrapper import SchemaEx

@pytest.fixture
def schex():
    return SchemaEx('schemas/2.2_ler.xsd')

def test_01(schex):
    assert len(schex.elements) == 26
