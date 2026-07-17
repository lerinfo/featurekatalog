#!/usr/bin/env python3
import re
from pathlib import Path

from xmlschema import XMLSchema
from flask import Flask, abort, current_app, render_template
from flask_frozen import Freezer
from markupsafe import Markup, escape

from featurekatalog import all_restriktioner, parse_featurekatalog
from wrapper import SchemaEx

DOCX_PATH = Path(__file__).parent / 'ler_featurekatalog.docx'
XSD_PATH = Path(__file__).parent / 'schemas' / '2.2_ler.xsd'
GML_ABSTRACT_TYPE = '{http://www.opengis.net/gml/3.2}AbstractGMLType'

# 2.2_ler.xsd imports both of these (LinearDimension, LinearAnnotation, TextAnnotation
# live here, not in the LER namespace itself) - schema.elements only holds ler.xsd's own
# namespace, so these three otherwise silently disappear from every XSD-derived page.
LER_FAMILY_NAMESPACES = {
    'http://data.gov.dk/schemas/LER/2/gml',
    'http://data.gov.dk/schemas/dimensions/2/gml',
    'http://data.gov.dk/schemas/annotations/2/gml',
}


def normalize_navn(navn):
    """ASCII-fold Danish names the same way the XSD's element names do
    (æ/ø/å -> ae/oe/aa), so docx-navne and XSD-elementnavne can be matched."""
    return navn.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = str(Path(__file__).parent / 'docs')
app.config['FREEZER_RELATIVE_URLS'] = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

_featuretyper = None
_schex = None
_type_tree = None
_chains = None
_element_details = None


def get_featuretyper():
    global _featuretyper
    if _featuretyper is None:
        _featuretyper = parse_featurekatalog(str(DOCX_PATH))
    return _featuretyper


def get_schex():
    global _schex
    if _schex is None:
        schex = SchemaEx(XMLSchema(str(XSD_PATH)))
        # SchemaEx's own type-hierarchy walk (built in __init__) only seeds from
        # schex.schema.elements (ler.xsd's own namespace). Extend it with every
        # element in the imported dimensions/annotations namespaces too, so Type
        # Tree/Type Chains cover them as well. _register_type_and_ancestors is
        # idempotent for already-registered types, so re-running it for the ler.xsd
        # elements too is harmless.
        for elm in schex.schema.maps.elements.values():
            if elm.target_namespace in LER_FAMILY_NAMESPACES:
                schex._register_type_and_ancestors(elm.type)
        _schex = schex
    return _schex


def get_all_xsd_elements():
    """Every element across LER + Dimensions + Annotations (not just ler.xsd's own
    namespace) - these are what the featurekatalog docx calls featuretyper."""
    schex = get_schex()
    return [
        elm for elm in schex.schema.maps.elements.values()
        if elm.target_namespace in LER_FAMILY_NAMESPACES
    ]


def get_xsd_element_by_navn(navn):
    target = normalize_navn(navn)
    for elm in get_all_xsd_elements():
        if normalize_navn(elm.local_name) == target:
            return elm
    return None


def get_type_tree():
    """List of (depth, xsdtype), walking the type hierarchy from AbstractGMLType down,
    filtered to only the types actually used by a featurekatalog featuretype (ie. the
    same 30 featuretyper documented in the docx) - not the ~85 other XSD-only types
    (kodelister, PropertyType wrappers, ...) that never appear in the docx."""
    global _type_tree
    if _type_tree is None:
        schex = get_schex()
        absgmltype = schex.maps.types[GML_ABSTRACT_TYPE]
        known_types = {elm.type for elm in get_all_xsd_elements()}
        _type_tree = [
            (depth, xsdtype)
            for depth, xsdtype in schex.walk_type_hierarchy(absgmltype)
            if xsdtype in known_types
        ]
    return _type_tree


def get_chains():
    """List of (xsdtype, [ancestors..., xsdtype]) for every type in the tree."""
    global _chains
    if _chains is None:
        schex = get_schex()
        chains = []
        for _depth, xsdtype in get_type_tree():
            chain = [xsdtype] + list(schex.iter_type_ancestors(xsdtype))
            chain.reverse()
            chains.append((xsdtype, chain))
        _chains = chains
    return _chains


def get_element_details():
    """List of {'elm': element, 'allowed_elms': [children...]} for every schema element."""
    global _element_details
    if _element_details is None:
        _element_details = [
            {'elm': elm, 'allowed_elms': list(elm.iterchildren())}
            for elm in get_all_xsd_elements()
        ]
    return _element_details


@app.template_filter('anchor')
def anchor_filter(prefixed_name):
    return prefixed_name.lower().replace(':', '-')


def get_by_navn(navn):
    for ft in get_featuretyper():
        if ft['navn'] == navn:
            return ft
    return None


def get_element_detail_by_slug(slug):
    for elmdict in get_element_details():
        if anchor_filter(elmdict['elm'].prefixed_name) == slug:
            return elmdict
    return None


def get_chain_by_slug(slug):
    for xsdtype, chain in get_chains():
        if anchor_filter(xsdtype.prefixed_name) == slug:
            return xsdtype, chain
    return None


@app.template_filter('linkify')
def linkify_filter(value):
    """Turn values like 'Ledning (Featuretype)' or plain 'Ledning' into a link,
    if 'Ledning' is a known featuretype."""
    if not isinstance(value, str):
        return value
    known_names = {ft['navn'] for ft in get_featuretyper()}
    match = re.match(r'^(.*?)(\s\(\w+\))?$', value, re.DOTALL)
    name, suffix = match.group(1), match.group(2) or ''
    if name in known_names:
        # Use the (possibly Frozen-Flask-patched, relative-URL-producing) url_for
        # from the Jinja globals, not flask.url_for directly - see freezer.register_generator
        # note in Frozen-Flask docs: relative_url_for only patches app.jinja_env.globals.
        jinja_url_for = current_app.jinja_env.globals['url_for']
        return Markup('<a href="{}">{}</a>{}').format(jinja_url_for('featuretype', navn=name), name, suffix)
    return escape(value)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/featuretype_list/')
def featuretype_list():
    grupper = {}
    for ft in get_featuretyper():
        ft = dict(ft)
        ft['xsd_elm'] = get_xsd_element_by_navn(ft['navn'])
        grupper.setdefault(ft['pakke'], []).append(ft)
    return render_template('featuretype_list.html', grupper=grupper.items())


@app.route('/featuretype/<navn>/')
def featuretype(navn):
    ft = get_by_navn(navn)
    if ft is None:
        abort(404)
    return render_template('featuretype.html', ft=ft)


@app.route('/restriktioner/')
def restriktioner():
    return render_template('restriktioner.html', restriktioner=all_restriktioner(get_featuretyper()))


@app.route('/element_details/<slug>/')
def element_detail(slug):
    elmdict = get_element_detail_by_slug(slug)
    if elmdict is None:
        abort(404)
    return render_template('element_detail.html', elmdict=elmdict)


@app.route('/featuretype_tree/')
def featuretype_tree():
    return render_template('featuretype_tree.html', schex=get_schex(), absgmltype_tree=get_type_tree())


@app.route('/typechain/<slug>/')
def typechain_detail(slug):
    result = get_chain_by_slug(slug)
    if result is None:
        abort(404)
    xsdtype, chain = result
    return render_template('typechain_detail.html', xsdtype=xsdtype, chain=chain)


@app.route('/general_constraints/')
def general_constraints():
    return render_template('general_constraints.html')


freezer = Freezer(app)


@freezer.register_generator
def featuretype_urls():
    for ft in get_featuretyper():
        yield 'featuretype', {'navn': ft['navn']}


@freezer.register_generator
def element_detail_urls():
    for elmdict in get_element_details():
        yield 'element_detail', {'slug': anchor_filter(elmdict['elm'].prefixed_name)}


@freezer.register_generator
def typechain_detail_urls():
    for xsdtype, _chain in get_chains():
        yield 'typechain_detail', {'slug': anchor_filter(xsdtype.prefixed_name)}


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'freeze':
        freezer.freeze()
        # Stop GitHub Pages from running the output through Jekyll.
        (Path(app.config['FREEZER_DESTINATION']) / '.nojekyll').touch()
        print(f'Frozen to {app.config["FREEZER_DESTINATION"]}')
    else:
        app.run(debug=True)
