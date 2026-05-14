# General constraints

Udover XSD constraints og listen med constraints ("restriktioner") fra featurekatalog / XMI, så er der nogle få yderligere.

## Alle geometrier skal angives i 3 dimensioner, dog kan der bruges -99 for Z

Jeg har ikke testet for nyligt, det bygger på min hukommelse.

Nogle steder er det tilladt at sætte Z=-99. Men det er aldrig tilladt kun at opgive to tal per vertex, ved at sætte srsDimension=2.

## Sæt srsDimension=3

Jeg har ikke testet. Men i alle deres eksempler har de eksplicit sat srsDimension=3. Kilde: https://ler.dk/Files/C0200_Vejledning_til_udfyldelse_af_GML_for_udveksling_af_ledningsoplysninger_v_1_23.pdf

## XML kommentarer ikke tilladt

Så vidt jeg husker, så fejler den uden en behjælpelig fejl, hvis det xml man sender indeholder xml kommentarer.

