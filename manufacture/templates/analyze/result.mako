<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyzer</h2>
<br />

Time required: ${time_required}<br />
<br />
Machine Sequences:<br />
% for m, notifications in machine_notifications.items():
    machine${m}<br />
    % for notif in notifications:
        ${notif}<br />
    % endfor
    <br />
% endfor
<br />
Test Output:<br />
<pre>${test_output}</pre><br />
<br />
<script type="text/javascript">

</script>
</%block>
