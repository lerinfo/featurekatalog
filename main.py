try:
    import os
    import sys
    from xmlschema import XMLSchema
    sys.path.insert(0, os.path.dirname(__file__))
    from wrapper import SchemaEx
    from pathlib import Path
    import yaml
except ImportError as e:
    
    raise Exception("Problem with imports, inside main.py", str(e))
    # Workaround for bug, to cause dramatic fail, see: 
    # https://github.com/fralau/mkdocs-macros-plugin/issues/285


def define_env(env):
    schema: XMLSchema = XMLSchema('schemas/2.2_ler.xsd')
    schex: SchemaEx = SchemaEx(schema)
    env.variables['schex'] = schex

    absgmltype = schex.maps.types['{http://www.opengis.net/gml/3.2}AbstractGMLType']
    tree = list(schex.walk_type_hierarchy(absgmltype))
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


    element_details = []
    for elm in schex.elements.values():
        element_details.append({
            'elm': elm,
            'allowed_elms': elm.iterchildren(),
        })
    env.variables['element_details'] = element_details

    # load constraints

    constraints_dir = Path("constraints")
    constraints = []
    for path in constraints_dir.glob("*.yml"):
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:  # skip empty files
                constraints.extend(data)
    env.variables['constraints'] = constraints