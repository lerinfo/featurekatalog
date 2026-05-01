# Element Details

This page shows a section for each XsdType, and in each section is shown the ancestry for that type.

{% for elmdict in element_details %}
<h2 id="{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}">{{elmdict.elm.prefixed_name}}</h2>
<a href="#{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}">#{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}</a>

<div>
<table class='tree-table'>
<tr>
<th>name</th>
<th>occurs</th>
<th>required</th>
<th>nillable</th>
</tr>
{% for subelm in elmdict.allowed_elms %}
<tr>
<td>
{{subelm.prefixed_name}}
</td>
<td>
{{subelm.occurs}}
</td>
<td>
{{'required' if (subelm.occurs[0] > 0) else ''}}
</td>
<td>
{{'nillable' if subelm.nillable else ''}}
</td>
</tr>
{% endfor %}
</table>
</div>

{% endfor %}
