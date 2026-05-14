# Constraints for feature types (fra Feature Katalog)

Jeg har gennemlæst Featurekatalog (docx) og kopieret/indtastet restriktioner, for et udvalg af feature types, 
i mit eget yaml-format, i filer i mappen constraints, e.g. constraints/Elledning.yml.

Det er dog ikke alle feature types, der er taget med.

Det er tydeligt, at docx er genereret ud fra en XMI fil. Det havde lettere og mere elegant at extracte constraints
fra disse XSI-filer, men det er ikke til at finde XMI filen på deres hjemmeside, og deres support har meddelt
at de ikke har nogen sådan fil.

Bemærk, at name ikke er unik; det er kun kombinationen af feature_type og name, der unikt identificerer en regel.

<table class='tree-table'>
<tr>
<th>feature_type</th>
<th>name</th>
<th>expression</th>

</tr>
{% for con in constraints %}
<tr>
<td class='mono'>
{{con.feature_type}}
</td>
<td class='mono'>
{{con.name}}
</td>
<td>
{{con.expression | replace('\n', '<br>') | safe }}
</td>

</tr>
{% endfor %}
</table>
