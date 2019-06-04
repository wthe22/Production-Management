<%inherit file="../base.mako" />


<%block name="content">

<h2>${heading}</h2>
<form id="edit_form" action="?" method="post" onsubmit="return model_edit_form.validate();">
    <div class="horizontal-list" id="model_edit"></div><br />
    <button type="submit" name="submit" value="submit">Submit</button>
</form>

<script type="text/javascript">
model_edit_form = new EditForm({
    ...{
        "varname": "model_edit_form",
        "id": "model_edit",
        "form": "edit_form"
    },
    ...${str(edit_form_schema) | n},
})
model_edit_form.load();
</script>
</%block>
