<%inherit file="../base.mako" />


<%block name="content">
<h2>Machines</h2>
<a href="${request.route_url('machine_new')}">New Machine</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Name</th><th>Quantity</th><th>Action</th></tr>
            % for machine in machine_list:
                <tr><td>${machine.id}</td>
                <td><a href="${request.route_url('machine_show', id=machine.id)}">${machine.name}</a></td>
                <td>${machine.quantity}</td>
                <td>
                    <a href="${request.route_url('machine_edit', id=machine.id)}">Edit</a>
                    <a href="${request.route_url('machine_delete', id=machine.id)}">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>