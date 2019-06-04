<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyzer</h2>
<br />
<form id="analyze_form" action="?" method="post" onsubmit="
    return (
        order_form.validate()
        && machine_form.validate()
    );
">
    <div class="horizontal-list">
        <h3>Item Orders</h3>
        <div id="order_list"></div>
    </div>
    <div class="horizontal-list" style="width:5%;"></div>
    <div class="horizontal-list">
        <h3>Allocated Machines</h3>
        <div id="machine_list"></div>
    </div>
    <br />
    <br />
    <button type="submit" name="submit" value="submit">Calculate sequence</button>
</form>
<br />
<br />

% if not message is None:
${message}<br />
<br />
% endif

% if view.has_previous_result:
    <input type="button" onclick="location.href='${request.route_url('analyzer_result')}';" value="Previous Result" /><br />
% endif
<br />
<input type="button" onclick="location.href='${request.route_url('analyzer_test')}';" value="Test" /><br />

<script type="text/javascript">
var debug = true
order_form = new ArrayForm({
    "form": "analyze_form",
    "varname": "order_form",
    "id": "order_list",
    "name": "orders",
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
order_form.load();
if (debug) {
    order_form.add_row([{value: 37}, {value: 150}]);
    order_form.add_row([{value: 38}, {value: 50}]);
    order_form.add_row([{value: 39}, {value: 189}]);
    order_form.add_row([{value: 41}, {value: 60}]);
    order_form.add_row([{value: 40}, {value: 123}]);
    order_form.add_row([{value: 76}, {value: 151}]);
    order_form.add_row([{value: 67}, {value: 10}]);
    order_form.add_row([{value: 66}, {value: 7}]);
} else {
    order_form.add_row();
}

machine_form = new ArrayForm({
    "form": "analyze_form",
    "varname": "machine_form",
    "id": "machine_list",
    "name": "machines",
    "components": [
        {
            "name": "",
            "description": "Machine",
            "type": "select",
            "options": ${str(machine_options) | n},
        },
        {
            "name": "",
            "description": "Quantity",
            "type": "number",
            "value": 0,
        },
    ],
});
machine_form.load();
if (debug) {
    machine_form.add_row([{value: 2}, {value: 4}]);
    machine_form.add_row([{value: 3}, {value: 2}]);
} else {
    order_form.add_row();
}

//${item_machine_list}

</script>
</%block>
