<%inherit file="../base.mako" />


<%block name="content">
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <h2>Items (${item_count})</h2>
        <a href="${request.route_url('item_new')}">New Item</a><br />
        <br />
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Item</th></tr>
            % for item in item_list:
                <tr>
                    <td>${item.id}</td>
                    <td><a href="${request.route_url('item_show', id=item.id)}">${item.name}</a></td>
                </tr>
            % endfor
        </table>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h2>Recipes (${recipe_count})</h2>
        <a href="${request.route_url('recipe_new')}">New Recipe</a><br />
        <br />
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Recipe</th><th>Input</th><th>Output</th></tr>
            % for recipe, column_list in recipe_full_list:
            <tr>
                <td>${recipe.id}</td>
                <td><a href="${request.route_url('recipe_show', id=recipe.id)}">${recipe.name}</td>
                % for input_output in column_list:
                    <td>
                    % for recipe_item in input_output:
                        % if not recipe_item == None:
                            <a href="${request.route_url('item_show', id=recipe_item.item_id)}">${recipe_item.quantity} ${recipe_item.item.name}</a><br />
                        % endif
                    % endfor
                    </td>
                % endfor
            </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
