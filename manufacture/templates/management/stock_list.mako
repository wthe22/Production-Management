<%inherit file="../base.mako" />


<%block name="content">
<h2>Inventory</h2>
<a href="${request.route_url('stock_new')}">New Stock</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Item</th><th>Quantity</th><th>Action</th></tr>
            % for stock in stock_list:
                <tr><td>${stock.id}</td>
                <td><a href="${request.route_url('item_show', id=stock.item.id)}">${stock.item.name}</a></td>
                <td>${stock.quantity}</td>
                <td>
                    <a href="${request.route_url('stock_edit', id=stock.id)}">Edit</a>
                    <a href="${request.route_url('stock_delete', id=stock.id)}">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
