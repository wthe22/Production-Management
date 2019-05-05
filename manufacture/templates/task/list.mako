<%inherit file="../base.mako" />


<%block name="content">
<h2>Task</h2>
<a href="/new/task/">New Task</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Machine</th><th>Recipe</th><th>Comment</th><th>Start time</th><th>End time</th><th>Action</th></tr>
            % for task in task_list:
                <tr><td>${task.id}</td>
                <td><a href="/machine/${task.machine.id}/">${task.machine.name}</a></td>
                <td><a href="/recipe/${task.recipe.id}/">${task.recipe.name}</a></td>
                <td>${task.comment}</td>
                <td>${task.start_time}</td>
                <td>${task.end_time}</td>
                <td>
                    <a href="/edit/task/${task.id}/">Edit</a>
                    <a href="/delete/task/${task.id}/">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>