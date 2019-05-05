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
        {id: "machine", desc: "Machine", type: "select", required: true, value: ${str(form_values['machine']) | n}},
        {id: "recipe", desc: "Recipe", type: "select", required: true, value: ${str(form_values['recipe']) | n}},
        {id: "comment", desc: "Comment", type: "text", required: false, value: "${form_values['comment']}"},
        {id: "start_time", desc: "Start Time", type: "number", required: true, value: ${form_values['start_time']}},
        {id: "end_time", desc: "End Time", type: "number", required: false, value: ${form_values['end_time']}},
    ],
);
model_edit_form.load();
</script>
</%block>
