# Element Details

This page shows a section for each XsdType, and in each section is shown the ancestry for that type.

{% for elmdict in element_details %}
<h2 id="{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}">{{elmdict.elm.prefixed_name}}</h2>
<a href="#{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}">#{{ elmdict.elm.prefixed_name | lower | replace(':', '-') }}</a>

<div class='helping_text'>
Shows the list from elm.iterchildren(). So that is all the children that may occur as child elements of elm. However, the list ignores the *composite types* (any, all, sequence). 
<ul>
<li>If all the included element types included have composite type=sequence, then elm behaves as having composite type=sequence for the list below</li>
<li>If all of the included element types have composite type=any, then elm behaves as having composite type=any for the list below</li>
<li>If all of the included element types have composite type=all, then elm behaves as having composite type=all for the list below</li>
<li>If the included element types have different composite types, then the list below wont tell exactly what is valid/invalid. You will need to look in elm.type.content.
</ul>

</div>

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
