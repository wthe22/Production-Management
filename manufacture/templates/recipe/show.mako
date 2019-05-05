<%inherit file="../base.mako" />


<%block name="content">
<h2>Recipe for ${recipe.name} (Recipe #${recipe.id})</h2>
<a href="/edit/recipe/${recipe.id}/">Edit</a>
<a href="/delete/recipe/${recipe.id}/">Delete</a>
<br />
<br />
<div style="width:100%; height:50%; display: flex;">
    <div class="horizontal-list">
        <h3>Information</h3>
        <table class="striped" style="width:100%;">
            <tr><td>ID</td><td>${recipe.id}</td></tr>
            <tr><td>Name</td><td>${recipe.name}</td></tr>
            <tr><td>Description</td><td>${recipe.description}</td></tr>
            <tr><td>Duration</td><td>${recipe.duration}</td></tr>
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Input</h3>
        <table class="striped" style="width:100%;">
            <tr><th>Item</th><th>Quantity</th></tr>
            % for recipe_item in recipe_input:
            <tr>
                <td><a href="/item/${recipe_item.item.id}/">${recipe_item.item.name}</a></td>
                <td>${recipe_item.quantity}</td>
            </tr>
            % endfor
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Output</h3>
        <table class="striped" style="width:100%;">
            <tr><th>Item</th><th>Quantity</th></tr>
            % for recipe_item in recipe_output:
            <tr>
                <td><a href="/item/${recipe_item.item.id}/">${recipe_item.item.name}</a></td>
                <td>${recipe_item.quantity}</td>
            </tr>
            % endfor
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Machines</h3>
        <table class="striped" style="width:100%;">
            <tr><th>Machine</th></tr>
            % for machine in machine_list:
            <tr>
                <td><a href="/machine/${machine.id}/">${machine.name}</a></td>
            </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
