# Elements

Elements cant be shown as a hierarchy (unlike a types). This list shows only elements in schema.elements, which holds only the elements defined in the target namespace of the schema. 

<table class='tree-table'>
<tr>
<th>element name</th>
<th>type name</th>
<th>abstract</th>
<th>details</th>

</tr>
{% for elm in schex.elements.values() %}
<tr>
<td class='mono'>
{{elm.prefixed_name}}
</td>
<td class='mono'>
{{elm.type.prefixed_name}}
</td>
<td class='flag'>
{{'abstract' if elm.type.abstract else ''}}
</td>
<td>
<a href="/typechain/#{{ elm.type.prefixed_name | lower | replace(':', '-') }}">elm</a> ///
<a href="/element_details/#{{ elm.type.prefixed_name | lower | replace(':', '-') }}">type</a>
</td>

</tr>
{% endfor %}
</table>
