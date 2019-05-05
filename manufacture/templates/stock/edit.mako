<%inherit file="../base.mako" />


<%block name="content">

<style>
.rows {
    width:100%;
    height:auto;
    overflow:hidden;
    margin: 5px;
}
.label {
    width:150px;
    float:left;
}
.required {
    color:#F00;
}
.input-row {
    width:250px;
    background-color:#FFF;
    float:left;
    position:relative;
}
</style>

<script type="text/javascript">
</script>

<h2>${heading}</h2>
<div class="horizontal-list" style="width: 40%" id="model_edit_form"></div>
<div class="horizontal-list" style="width: 30%">
</div>

<script type="text/javascript">
model_edit_form = new EditForm(
    "model_edit_form",
    [
        {id: "item", desc: "Item", type: "select", required: true, value: ${str(form_values['item']) | n}},
        {id: "comment", desc: "Comment", type: "text", required: true, value: "${form_values['comment']}"},
        {id: "description", desc: "Description", type: "text", required: false, value: "${form_values['description']}"},
        {id: "quantity", desc: "Quantity", type: "number", required: true, value: ${form_values['quantity']}},
    ],
);
model_edit_form.load();
</script>
</%block>
