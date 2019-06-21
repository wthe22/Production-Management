<%inherit file="../base.mako" />

<%!
import time
time_format = "%Y-%m-%d %H:%M:%S"
%>


<%block name="content">
<h2>Task</h2>
<a href="${request.route_url('task_new')}">New Task</a><br />
<br />
<div style="width:100%;">
    <table class="striped">
        <tr><th>ID</th><th>Recipe</th><th>Cycles</th><th>Description</th><th>Action</th></tr>
        % for task in task_list:
            <tr>
                <td>${task.id}</td>
                <td><a href="${request.route_url('recipe_show', id=task.recipe_id)}">${task.recipe.name}</a></td>
                <td>${task.cycles}</td>
                <td>${task.description}</td>
                <td><a href="${request.route_url('task_delete', id=task.id)}">Delete</a></td>
            </tr>
        % endfor
    </table>
</div>
<br />

<div style="width:100%;">
    <h2>Machine Task</h2>
    <table class="striped">
        <tr><th>ID</th><th>Machine</th><th>Task</th><th>Start time</th><th>Cycles</th><th>Action</th></tr>
        % for machine_task in machine_task_list:
            <tr>
                <td>${machine_task.id}</td>
                <td>${machine_task.machine.name}</td>
                <td>#${machine_task.task_id}: ${machine_task.task.recipe} (x${machine_task.cycles})</td>
                <td>${time.strftime(time_format, time.localtime(machine_task.start_time))}</td>
                <td>${machine_task.cycles}</td>
                <td><a href="${request.route_url('machine_task_delete', id=machine_task.id)}">Delete</a></td>
            </tr>
        % endfor
    </table>
</div>
<br />
</%block>
