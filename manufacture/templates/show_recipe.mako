<%inherit file="base.mako" />


<%block name="content">
<h2>Recipe for ${recipe.name} (Recipe #${recipe.id})</h2>
<a href="/edit/recipe/${recipe.id}/">Edit</a><br />
<br />
<div style="width:100%; height:50%; display: flex;">
    <div class="horizontal-list">
        <h3>Information</h3>
        <table class="striped" style="width:100%;">
            <tr><td>ID</td><td>${recipe.id}</td></tr>
            <tr><td>Name</td><td>${recipe.name}</td></tr>
            <tr><td>Description</td><td>${recipe.description}</td></tr>
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Input</h3>
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Item</th></tr>
            % for recipe_item in recipe_input:
            <tr>
                <td>${recipe_item.item.id}</td>
                <td>${recipe_item.quantity} <a href="/item/${recipe_item.item.id}/">${recipe_item.item.name}</a></td>
            </tr>
            % endfor
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Output</h3>
        <table class="striped" style="width:100%;">
            <tr><th>RI.ID</th><th>ID</th><th>Item</th></tr>
            % for recipe_item in recipe_output:
            <tr>
                <td>${recipe_item.id}</td>
                <td>${recipe_item.item.id}</td>
                <td>${recipe_item.quantity} <a href="/item/${recipe_item.item.id}/">${recipe_item.item.name}</a></td>
            </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
