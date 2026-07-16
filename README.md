# featurekatalog

Jeg har tit haft brug for at tjekke, hvad der var tilladt ift LER,
herunder hvornår hvilke attributter var påkrævede, og jeg syntes
det var besværligt/trægt at læse den officielle LER-dokumentation.

Jeg har samlet ovenstående information i en hjemmeside, hér.

## Detaljer omkr udarbejdelsen af denne dokumentation

Al dokumentation genereres som statisk html. Disse html filer
er autogeneret vha Flask og Frozen-Flask plus mine egne
værktøjer (med hjælp fra Claude AI), der extracter info fra resourcer.

Der er tre typer af information/krav, fra tre forskellige kilder:

## Komposition af data

### XML Schema / XSD

Information omkr struktur/komposition er extracted fra XSD-filer.

### Restriktioner, attributter, m.m. fra featurekatalog

I LER's featurekatalog docx angives for hver feature type diverse
informationer i et bestemt format. Disse parses/extractes og vises
også.

### Yderligere restriktioner

Der er andre krav, som enten slet ikke er dokumenteret eller som
er dokumenteret på en måde, hvor de ikke kommer med i min
parsing af ovennævnte docx.

- `featurekatalog.py` parser `ler_featurekatalog.docx` (attributter, restriktioner,
  associationsroller pr. featuretype).
- `wrapper.py` (`SchemaEx`) parser `schemas/2.2_ler.xsd` (og de importerede
  Dimensions/Annotations-namespaces) for XSD-struktur (elementer, typehierarki).
- `app.py` fletter de to og server dem som én sammenhængende Flask-app.

## How to build

For at bygge disse statiske sider.

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
