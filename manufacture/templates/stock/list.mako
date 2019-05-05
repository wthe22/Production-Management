<%inherit file="../base.mako" />


<%block name="content">
<h2>Inventory</h2>
<a href="/new/stock/">New Stock</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Item</th><th>Comment</th><th>Quantity</th><th>Action</th></tr>
            % for stock in stock_list:
                <tr><td>${stock.id}</td>
                <td><a href="/item/${stock.item.id}/">${stock.item.name}</a></td>
                <td>${stock.comment}</td>
                <td>${stock.quantity}</td>
                <td>
                    <a href="/edit/stock/${stock.id}/">Edit</a>
                    <a href="/delete/stock/${stock.id}/">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
