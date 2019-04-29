<%inherit file="base.mako" />


<%block name="content">
<h2>{{ object_type }}</h2>
<form method="POST" class="django-form">
    {% csrf_token %}
    <table>
    {{ form.as_table }}
    </table>
    <button type="submit" class="save btn btn-default">Save</button>
</form>
</%block>