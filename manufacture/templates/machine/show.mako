<%inherit file="../base.mako" />


<%block name="content">
<h2>${machine.name} Machine</h2>
<a href="${request.route_url('machine_edit', id=machine.id)}">Edit</a>
<a href="${request.route_url('machine_delete', id=machine.id)}">Delete</a>
<br />
<br />
<div style="width:100%; height:50%; display: flex;">
    <div class="horizontal-list">
        <h3>Information</h3>
        <table class="striped" style="width:100%;">
            <tr><td>ID</td><td>${machine.id}</td></tr>
            <tr><td>Name</td><td>${machine.name}</td></tr>
            <tr><td>Details</td><td>${machine.details}</td></tr>
            <tr><td>Quantity</td><td>${machine.quantity}</td></tr>
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Producible Recipes</h3>
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Name</th></tr>
            % for recipe in recipe_list:
            <tr>
                <td>${recipe.id}</td>
                <td><a href="${request.route_url('recipe_show', id=recipe.id)}">${recipe.name}</a></td>
            </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
