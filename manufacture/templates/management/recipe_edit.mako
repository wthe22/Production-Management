<%inherit file="../base.mako" />


<%block name="content">

<h2>${heading}</h2>
<form id="edit_form" action="?" method="post" onsubmit="
    return (
        model_edit_form.validate()
        && recipe_input_form.validate()
        && recipe_output_form.validate()
    );
">
    <div class="horizontal-list" id="model_edit"></div><br />
    <div class="horizontal-list">
        <h3>Input items</h3>
        <div id="recipe_input_list"></div>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Output items</h3>
        <div class="horizontal-list" id="recipe_output_list"></div>
    </div>
    <br />
    <br />
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

recipe_input_form = new ArrayForm({
    "form": "edit_form",
    "varname": "recipe_input_form",
    "id": "recipe_input_list",
    "name": "recipe_inputs",
    "components": [
        {
            "name": "",
            "description": "Item",
            "type": "select",
            "options": ${str(item_options) | n},
        },
        {
            "name": "",
            "description": "Quantity",
            "type": "number",
            "value": 0,
        },
    ],
});
recipe_input_form.load();
% if len(recipe_input) == 0:
    recipe_input_form.add_row();
% else:
    % for recipe_item in recipe_input:
        recipe_input_form.add_row([{value: ${recipe_item.item_id}}, {value: ${recipe_item.quantity}}]);
    % endfor
% endif

recipe_output_form = new ArrayForm({
    "form": "edit_form",
    "varname": "recipe_output_form",
    "id": "recipe_output_list",
    "name": "recipe_outputs",
    "components": [
        {
            "name": "",
            "description": "Item",
            "type": "select",
            "options": ${str(item_options) | n},
        },
        {
            "name": "",
            "description": "Quantity",
            "type": "number",
            "value": 0,
        },
    ],
});
recipe_output_form.load();
% if len(recipe_output) == 0:
    recipe_output_form.add_row();
% else:
    % for recipe_item in recipe_output:
        recipe_output_form.add_row([{value: ${recipe_item.item_id}}, {value: ${recipe_item.quantity}}]);
    % endfor
% endif

</script>
</%block>
