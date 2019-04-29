<%inherit file="base.mako" />


<%block name="content">
<h2>Inventory</h2>
<a href="/new/stock/">New Item</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Item</th><th>Description</th><th>Quantity</th><th>Action</th></tr>
            % for stock in stock_list:
                <tr><td>${stock.id}</td>
                <td><a href="/stock/${stock.id}">${stock.item.name}</a></td>
                <td>${stock.description}</td>
                <td>${stock.quantity}</td>
                <td>
                    <a href="/edit/stock/${stock.id}">Edit</a>
                    <a href="/delete/stock/${stock.id}">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
