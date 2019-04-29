<%inherit file="base.mako" />


<%block name="content">
<script type="text/javascript">
function reload_iframe(id, link) {
    console.log("ID: " + id);
    console.log("Link: " + link);
    document.getElementById(id).src = link;
}
</script>

<h2>Database Samples</h2>
<div>
    <fieldset class="horizontal-list">
        <legend>Hayday</legend>
        <button onclick="reload_iframe('output_box', '/populate/items/hayday/')">Core</button><br />
    </fieldset>
    <fieldset class="horizontal-list">
        <legend>Deeptown</legend>
        <button onclick="reload_iframe('output_box', '/populate/items/deeptown/')">Core</button><br />
        <button onclick="reload_iframe('output_box', '/populate/stocks/deeptown/' %}')">Stock</button><br />
    </fieldset>
</div>
<h3>Output</h3>
<iframe id="output_box" style="width:100%;"></iframe>
</%block>