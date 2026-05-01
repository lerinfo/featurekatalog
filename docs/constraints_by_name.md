# Constraints

Som Constraints, men sorteret efter `name`.

<table class='tree-table'>
<tr>
<th>feature_type</th>
<th>name</th>
<th>expression</th>

</tr>
{% for con in constraints | sort(attribute='name') %}
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
