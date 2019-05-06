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
<div class="horizontal-list" style="width: 50%" id="model_edit_form"></div>


<script type="text/javascript">
model_edit_form = new EditForm("model_edit_form", ${str(edit_form_schema) | n})
model_edit_form.load();
</script>
</%block>
