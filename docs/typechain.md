# Type Ancestry

This page shows a section for each XsdType, and in each section is shown the ancestry for that type.

{% for (xsdtype, chain) in chains %}
<h2 id="{{ xsdtype.prefixed_name | lower | replace(':', '-') }}">{{xsdtype.prefixed_name}}</h2>
<a href="#{{ xsdtype.prefixed_name | lower | replace(':', '-') }}">#{{ xsdtype.prefixed_name | lower | replace(':', '-') }}</a>
<div>
<table class='tree-table'>
<tr>
<th>name</th>
<th>abstract</th>
</tr>
{% for row in chain %}
<tr>
<td>
{{row.prefixed_name}}
</td>
<td>
{{'abstract' if row.abstract else ''}}
</td>
</tr>
{% endfor %}
</table>
</div>

{% endfor %}
