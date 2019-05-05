<%inherit file="base.mako" />


<%block name="content">
<h2>${item.name}</h2>
<a href="/edit/item/${item.id}/">Edit</a>
<a href="/delete/item/${item.id}/">Delete</a>
<br />
<br />
<div style="width:100%; height:50%; display: flex;">
    <div class="horizontal-list">
        <h3>Information</h3>
        <table class="striped" style="width:100%;">
            <tr><td>ID</td><td>${item.id}</td></tr>
            <tr><td>Name</td><td>${item.name}</td></tr>
            <tr><td>Description</td><td>${item.description}</td></tr>
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Recipes</h3>
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Recipe</th><th>Quantity</th></tr>
            % for recipe_item in recipe_output:
            <tr>
                <td>${recipe_item.recipe.id}</td>
                <td><a href="/recipe/${recipe_item.recipe.id}/">${recipe_item.recipe.name}</a></td>
                <td>${recipe_item.quantity}</td>
            </tr>
            % endfor
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Used in Recipes</h3>
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Recipe</th><th>Quantity</th></tr>
            % for recipe_item in recipe_input:
            <tr>
                <td>${recipe_item.recipe.id}</td>
                <td><a href="/recipe/${recipe_item.recipe.id}/">${recipe_item.recipe.name}</a></td>
                <td>${recipe_item.quantity}</td>
            </tr>
            % endfor
        </table>
    </div>
</div>
</%block>