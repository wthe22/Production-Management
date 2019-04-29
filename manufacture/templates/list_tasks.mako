<%inherit file="base.mako" />


<%block name="content">
<h2>Inventory</h2>
<a href="/new/task/">New Task</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Machine</th><th>Task</th><th>Recipe</th><th>Start time</th><th>End time</th><th>Action</th></tr>
            % for task in task_list:
                <tr><td>${task.id}</td>
                <td>${task.machine.name}</td>
                <td>${task.description}</td>
                <td>${task.recipe.name}</td>
                <td>${task.start_time}</td>
                <td>${task.end_time}</td>
                <td>
                    <a href="/edit/task/${task.id}">Edit</a>
                    <a href="/delete/task/${task.id}">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
