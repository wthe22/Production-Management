<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyze Result</h2>
<br />

Time required: ${time_required}<br />
<br />
Machine Sequences:<br />
% for m, notifications in machine_notifications.items():
machine${m}
<table class="striped">
    <tr>
        <th>Time</th>
        <th>Description</th>
    </tr>
    % for notif in notifications:
        <tr>
            <td>${notif.time}</td>
            <td>${notif.description}</td>
        </tr>
    % endfor
</table>
<br />
% endfor
<br />

<form id="apply_form" action="?" method="post" onsubmit="return true">
    <button type="submit" name="submit" value="submit">Start</button>
</form>

<br />
Test Output:<br />
<pre>${test_output}</pre><br />
<br />
<script type="text/javascript">

</script>
</%block>
