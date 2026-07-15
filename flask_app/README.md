# flask_app — v1 prototype

Erstatter (til evaluering) mkdocs-udgaven af kavaler. Bygger på Flask + Frozen-Flask
i stedet for mkdocs-macros, og Bootstrap i stedet for Material.

Kun featurekatalog-data er portet indtil videre (featuretyper, attributter,
associationsroller, restriktioner, via `featurekatalog.py` — kopieret fra
featurekatalog-repoet). XSD-baserede sider (Elements, Element Details, Type Tree,
Type Chains) er **ikke** portet endnu.

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
