# featurekatalog

Slå op hvad der er tilladt i LER-modellen, uden at skulle læse XSD'en eller
featurekatalog-docx'en direkte. Flask + Frozen-Flask (Bootstrap), i stedet for
mkdocs.

- `featurekatalog.py` parser `ler_featurekatalog.docx` (attributter, restriktioner,
  associationsroller pr. featuretype).
- `wrapper.py` (`SchemaEx`) parser `schemas/2.2_ler.xsd` (og de importerede
  Dimensions/Annotations-namespaces) for XSD-struktur (elementer, typehierarki).
- `app.py` fletter de to og server dem som én sammenhængende Flask-app.

## Udvikling

```bash
pip install -r requirements.txt
python3 app.py
```

Kører en almindelig Flask dev-server med hot reload på http://127.0.0.1:5000/.

## Byg statisk site

```bash
python3 app.py freeze
```

Skriver statisk HTML til `build/` (via Frozen-Flask). Klar til at committes og
hostes, fx via GitHub Pages.
