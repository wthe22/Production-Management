<%inherit file="../base.mako" />


<%block name="content">
<h2>Analyze Result</h2>
<br />

Time required: ${time_required}<br />
<br />
<h2>Task List</h2>
<table class="striped">
    <tr>
        <th>ID</th>
        <th>Recipe</th>
        <th>Cycles</th>
    </tr>
% for t, task in task_list.items():
    <tr>
        <td>${t}</td>
        <td>${task.recipe}</td>
        <td>${task.cycles}</td>
    </tr>
% endfor
</table>
<br />

<h2>Machine Task Distribution</h2>
% for m, notifications in machine_sequences.items():
<div class="horizontal-list">
    <h3>${machine_list[m].machine} (#${m})</h3>
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
</div>
<div class="horizontal-list" style="width:5%;"></div>
% endfor
<br />

<form id="apply_form" action="?" method="post" onsubmit="return true">
    <button type="submit" name="submit" value="submit">Start</button>
</form>
<br />

<table class="striped">
    <tr>
        <th>Time</th>
        <th>Description</th>
    </tr>
    % for notif in all_notifications:
        <tr>
            <td>${notif.time}</td>
            <td>${notif.description}</td>
        </tr>
    % endfor
</table>
<br />

<script type="text/javascript">

</script>
</%block>
