# Type Tree

schema.url: {{schex.schema.url}}


<table class='tree-table'>
<tr>
<th>name</th>
<th>type</th>
<th>abstract</th>
<th>typechain</th>

</tr>
{% for depth, xsdtype in absgmltype_tree %}
<tr>
<td class='mono' style='padding-left: {{20+depth*30}}px;'>
{{xsdtype.prefixed_name}}
</td>
<td class='mono'>
{{xsdtype.__class__.__name__}}
</td>
<td class='flag'>
{{'abstract' if xsdtype.abstract else ''}}
</td>
<td>
<a href="/typechain/#{{ xsdtype.prefixed_name | lower | replace(':', '-') }}">typechain</a>
</td>

</tr>
{% endfor %}
</table>
