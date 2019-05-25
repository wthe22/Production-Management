<%inherit file="../base.mako" />

<%!
import time
time_format = "%Y-%m-%d %H:%M"
%>


<%block name="content">
<h2>Task</h2>
<a href="${request.route_url('task_new')}">New Task</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Recipe</th><th>Cycles</th><th>Action</th></tr>
            % for task in task_list:
                <tr><td>${task.id}</td>
                <td><a href="${request.route_url('recipe_show', id=task.recipe_id)}">${task.recipe.name}</a></td>
                <td>${task.cycles}</td>
                <td>${task.description}</td>
                <td>
                    <a href="${request.route_url('task_edit', id=task.id)}">Edit</a>
                    <a href="${request.route_url('task_delete', id=task.id)}">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
