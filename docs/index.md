# Home

<p>
Som i kava + LER!
</p>

<p>
Jeg har lavet et lille værktøj vha Python / mkdocs, som generer nærværende dokumentation for LER-modellen, aka Feature Modelle, for LER 2.0. 
</p>

<p>
Værktøjet kigger alene på XSD-filerne. LER-modellen indeholder nogle krav, som ikke er implementeret i XSD, så der kan være krav udover dét, der er opremset heri.
</p>


<h5>Fremtidige forbedringer:</h5>
<p>
<ul>
<li>Tilføjelse af yderligere krav, altså de krav, som services.ler.dk har, men som ikke er implementeret i XSD</li>
<li>Mulighed for at cut and paste et stykke xml for en feature, og få øjeblikkeligt svar på, om det validerer ift XSD. Og gerne også, om det validerer ift yderligere krav på services.ler.dk. </li>
</ul>
</p>

<h5>Tekniske detaljer:</h5>
<p>
<ul>
<li>Tilføjelse af yderligere krav, altså de krav, som services.ler.dk har, men som ikke er implementeret i XSD</li>
<li>Mulighed for at cut and paste et stykke xml for en feature, og få øjeblikkeligt svar på, om det validerer ift XSD. Og gerne også, om det validerer ift yderligere krav på services.ler.dk. </li>
</ul>
</p>

#### Hvad kan man bruge det til?

Lad os sige, at du skal oprette eller tilpasse en databasemodel, således at den har de nødvendige oplysninger til at svare på LER-henvendelser. Vi antager, at det er en vandledning. Gå til [Elements](http://localhost:8000/elements/), find den rette linie med vandledning. Den viser, at elementtypen hedder `Vandledning` og den er er defineret til at have den globale navngivne type `VandledningType`. På linien kan du finde to links, `elm` for at se detaljer om elementet, og `type` for at se detaljer om typen. 

Klik på `elm`, og så kommer du til siden Element Details, direkte til afsnittet for dette element [link](http://localhost:8000/element_details/#ler-vandledning).

Her kan du se en tabel, med 38 rækker, én for hver af de 38 elementer, der kan være indeholdt i et Vandledning-element. Der kan faktisk være mere end 38 elementer, da nogle af dem er tilladt at være der mere end én gang. 

Antallet af forekomster af et givent element er angivet i kolonnen `occurs`. 

<ul>
<li>(1,1) præcist ét</li>
<li>(0,1) nul eller ét</li>
<li>(0,2) nul, ét eller to</li>
<li>(0,*) vilkårligt antal, inkl nul</li>
<li>(1,*) mindst én</li>
</ul>

For alle dem, hvor der skal være mindst én, så er rækken også markeret med `required`.

Blandt nogle af dem, som er required, er det dog stadigt muligt at sætte værdien til nil. Det svarer cirka til null/None i andre programmeringssprog. Og for personer, der ikke har prøvet at programmere, så svarer det cirka til "ingenting" eller "ingen værdi".

Lad os tage driftsstatus som eksempel.

    ler:driftsstatus | (1, 1) | required | nillable

Den er altså påkrævet, men må gerne være nil. Man kunne så tro, at man satte den til nil som følger:

    <ler:driftsstatus></driftsstatus>

Men blot fordi den ikke har nogen børn, det er ikke det samme som nil i XSD kontekst. For at sætte den til nil, er man nødt til at give den en særlig "magisk" attribut:

    <ler:driftsstatus xsi:nil="true"></driftsstatus>

Hvis man har tilføjet denne magiske attribut, så er det ikke tilladt (uanset, hvad et schema ellers siger) at have nogen child elements:

    <ler:driftsstatus xsi:nil="true">i drift</driftsstatus> <!-- INVALID -->

Så vidt jeg husker, så er driftsstatus påkrævet af LER-api, selvom det ikke er påkrævet af deres XSD.

