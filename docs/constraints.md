# Constraints

Jeg har gennemlæst Featurekatalog (docx) og kopieret/indtastet restriktioner, for et udvalg af feature types, 
i mit eget yaml-format, i filer i mappen constraints, e.g. constraints/Elledning.yml.

Det er dog ikke alle feature types, der er taget med.

Når jeg får fat i XMI-filer, så giver det nok mest mening at generere mine yml-filer dér fra.

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
