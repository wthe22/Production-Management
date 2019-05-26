<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyzer</h2>
<br />
<input type="button" onclick="location.href='${request.route_url('analyzer_test')}';" value="Test" /><br />
<input type="button" onclick="location.href='${request.route_url('analyzer_result')}';" value="Previous Result" /><br />
<br />
<form id="analyze_form" action="?" method="post" onsubmit="
    return (
        order_form.validate()
        && machine_form.validate()
    );
">
<div class="horizontal-list">
    <input type="hidden" value="" id="orders" name="orders">
    <table class="striped">
        <tr>
            <th>Item</th>
            <th>Amount</th>
            <th>Action</th>
        </tr>
        <tr>
            <td>Copper Nail</td>
            <td>150</td>
            <input type="hidden" value="37" name="orders__[0][]">
            <input type="hidden" value="150" name="orders__[0][]">
        </tr>
        <tr>
            <td>Copper Wire</td>
            <td>100</td>
            <input type="hidden" value="38" name="orders__[1][]">
            <input type="hidden" value="50" name="orders__[1][]">
        </tr>
        <tr>
            <td>Battery</td>
            <td>189</td>
            <input type="hidden" value="39" name="orders__[2][]">
            <input type="hidden" value="189" name="orders__[2][]">
        </tr>
        <tr>
            <td>Lamp</td>
            <td>60</td>
            <input type="hidden" value="41" name="orders__[3][]">
            <input type="hidden" value="60" name="orders__[3][]">
        </tr>
        <tr>
            <td>Circuit</td>
            <td>123</td>
            <input type="hidden" value="40" name="orders__[4][]">
            <input type="hidden" value="123" name="orders__[4][]">
        </tr>
        <tr>
            <td>Gunpowder</td>
            <td>20</td>
            <input type="hidden" value="76" name="orders__[5][]">
            <input type="hidden" value="151" name="orders__[5][]">
        </tr>
        <tr>
            <td>Hydrogen</td>
            <td>10</td>
            <input type="hidden" value="67" name="orders__[6][]">
            <input type="hidden" value="10" name="orders__[6][]">
        </tr>
        <tr>
            <td>Clean Water</td>
            <td>7</td>
            <input type="hidden" value="66" name="orders__[7][]">
            <input type="hidden" value="7" name="orders__[7][]">
        </tr>
    </table>
</div>
<div class="horizontal-list" style="width:5%;"></div>
<div class="horizontal-list">
    <input type="hidden" value="" id="machines" name="machines">
    <table class="striped">
        <tr>
            <th>Machine</th>
            <th>Amount</th>
            <th>Action</th>
        </tr>
        <tr>
            <td>Crafting</td>
            <td>4</td>
            <input type="hidden" value="2" name="machines__[0][]">
            <input type="hidden" value="4" name="machines__[0][]">
        </tr>
        <tr>
            <td>Chemistry</td>
            <td>2</td>
            <input type="hidden" value="3" name="machines__[1][]">
            <input type="hidden" value="2" name="machines__[1][]">
        </tr>
    </table>
</div>
<br />
<br />
<button type="submit" name="submit" value="submit">Submit</button>
</form>
<br />
<h2>Message</h2>
${message}<br />
<br />
<br />
<h2>Producable Items</h2>
<table class="striped">
    <tr>
        <td>ID</td>
        <td>Item Name</td>
    </tr>
% for item in item_list:
    <tr>
        <td>${item.id}</td>
        <td>${item.name}</td>
    </tr>
% endfor
</table>
<br />

<h2>Machine List</h2>
<table class="striped">
    <tr>
        <td>ID</td>
        <td>Machine Name</td>
        <td>Quantity</td>
    </tr>
% for machine in machine_list:
    <tr>
        <td>${machine.id}</td>
        <td>${machine.name}</td>
        <td>${machine.quantity}</td>
    </tr>
% endfor
</table>
<br />

<h2>Item Machine List</h2>
${item_machine_list}


<script type="text/javascript">
order_form = new ArrayForm("analyze_form", "orders")
machine_form = new ArrayForm("analyze_form", "machines")
</script>
</%block>
