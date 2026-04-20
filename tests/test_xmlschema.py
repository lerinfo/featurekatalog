from collections.abc import Mapping

import pytest
from wrapper import SchemaEx
import xmlschema.namespaces
from xmlschema.validators import XsdElement

'''
Not really testing anything, just used to experiment,
in order to understand how xmlschema works.
'''

@pytest.fixture
def schex():
    return SchemaEx('schemas/2.2_ler.xsd')


def test_01(schex):
    root_elms = schex.elements
    assert type(root_elms) == xmlschema.namespaces.NamespaceView
    assert isinstance(root_elms, Mapping)
    for k in root_elms.keys():
        assert isinstance(k, str)
    for v in root_elms.values():
        assert type(v) == XsdElement
    assert len(root_elms) == 26


def test_02(schex):
    children = list(schex.iterchildren())
    for c in children:
        assert type(c) == XsdElement
    assert len(children) == 26
