<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyzer</h2>
<br />
<input type="button" onclick="location.href='${request.route_url('analyzer_test')}';" value="Test" /><br />
<br />
<form id="analyze_form" action="${request.route_url('analyzer_result')}" method="post" onsubmit="
    return (
        order_form.validate()
        && machine_form.validate()
    );
">
<div class="horizontal-list">
    <input type="hidden" value="" id="orders" name="orders">
    <table class="striped">
        <tbody>
            <tr>
                <td>150 Copper Nail</td>
                <td><input type="hidden" value="37" name="orders__[0][]"></td>
                <td><input type="hidden" value="150" name="orders__[0][]"></td>
            </tr>
            <tr>
                <td>100 Copper Wire</td>
                <td><input type="hidden" value="38" name="orders__[1][]"></td>
                <td><input type="hidden" value="50" name="orders__[1][]"></td>
            </tr>
            <tr>
                <td>189 Battery</td>
                <td><input type="hidden" value="39" name="orders__[2][]"></td>
                <td><input type="hidden" value="189" name="orders__[2][]"></td>
            </tr>
            <tr>
                <td>60 Lamp</td>
                <td><input type="hidden" value="41" name="orders__[3][]"></td>
                <td><input type="hidden" value="60" name="orders__[3][]"></td>
            </tr>
            <tr>
                <td>123 Circuit</td>
                <td><input type="hidden" value="40" name="orders__[4][]"></td>
                <td><input type="hidden" value="123" name="orders__[4][]"></td>
            </tr>
            <tr>
                <td>20 Gunpowder</td>
                <td><input type="hidden" value="76" name="orders__[5][]"></td>
                <td><input type="hidden" value="151" name="orders__[5][]"></td>
            </tr>
            <tr>
                <td>10 Hydrogen</td>
                <td><input type="hidden" value="67" name="orders__[6][]"></td>
                <td><input type="hidden" value="10" name="orders__[6][]"></td>
            </tr>
            <tr>
                <td>7 Clean Water</td>
                <td><input type="hidden" value="66" name="orders__[7][]"></td>
                <td><input type="hidden" value="7" name="orders__[7][]"></td>
            </tr>
        </tbody>
    </table>
</div>
<div class="horizontal-list">
    <input type="hidden" value="" id="machines" name="machines">
    <table class="striped">
        <tbody>
            <tr>
                <td>4 Crafting</td>
                <td><input type="hidden" value="2" name="machines__[0][]"></td>
                <td><input type="hidden" value="4" name="machines__[0][]"></td>
            </tr>
            <tr>
                <td>2 Chemistry</td>
                <td><input type="hidden" value="3" name="machines__[1][]"></td>
                <td><input type="hidden" value="2" name="machines__[1][]"></td>
            </tr>
        </tbody>
    </table>
</div>
<br />
<br />
<button type="submit" name="submit" value="submit">Submit</button>
</form>

<script type="text/javascript">
order_form = new ArrayForm("analyze_form", "orders")
machine_form = new ArrayForm("analyze_form", "machines")
</script>
</%block>
