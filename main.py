try:
    import os
    import sys
    from xmlschema import XMLSchema
    sys.path.insert(0, os.path.dirname(__file__))
    from wrapper import SchemaEx
except ImportError:
    raise Exception("Problem with imports, inside main.py")
    # Workaround for bug, to cause dramatic fail, see: 
    # https://github.com/fralau/mkdocs-macros-plugin/issues/285


def define_env(env):
    schema: XMLSchema = XMLSchema('schemas/2.2_ler.xsd')
    schex: SchemaEx = SchemaEx(schema)
    env.variables['schex'] = schex

    absgmltype = schex.maps.types['{http://www.opengis.net/gml/3.2}AbstractGMLType']
    tree = list(schex.iter_type_tree(absgmltype))
    env.variables['absgmltype_tree'] = tree

    chains = []
    for depth,xsdtype in tree:
        l = [xsdtype] + list(schex.iter_type_ancestors(xsdtype))
        l.reverse()
        chains.append((
            xsdtype, 
            l,
        ))
    print('foo')
    env.variables['chains'] = chains
