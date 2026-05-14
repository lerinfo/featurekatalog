# Om mine LER-repositories

Jeg har arbejdet en del med LER, og har delt alt mit arbejde op i fire repositories:

* kavaler
* ler_xml_validator
* lermodel
* clay

## kavaler

Jeg er tit blevet lidt forvirret / frustreret over at finde rundt i og læse LER's officielle dokumentation. Derfor har jeg samlet noget af det på denne side, og formateret det på den måde, som giver mening for mig.

Det er ren dokumentation. Dog er der også lidt kode til at samle og præsentere dokumentationen. 

## lerxml

LER har publiceret nogle XSD. XSD egner sig fint til struktur, men ikke til forretningsregler; til gengæld er Schematron beregnet til at implementere sådanne forretningsregler.

Jeg har taget alle forretningsreglerne fra featurekataloget og implementeret dem i Schematron. 

Mappen indeholder python-kode, inkl en simpel CLI, som kan validere XML.

## lermodel

En mapping fra LERs officielle Featurekatalog / XML-format til mit eget yaml-format.

Repo indeholder værktøjer til:
* oversæt xml til yml
* oversæt yml til xml
* valider yml
* valider database table schema jvf mit format

## clay

En webservice, der kan svare på LER-forespørgsler. Den benytter sig af lermodel. 

Den benytter også, i mindre grad, ler_xml_validator, bl.a. til unit tests.


## Obsolete / abandoned repos

* lervalidator (forår 2024)
* ler_json_model (forår 2026)
* arcilla 
* arcilla2
* arcilla_watchdog
* arcilla_favrskov
* qler_validator (checks that db table schema matches qler expectations)
