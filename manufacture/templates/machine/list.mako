<%inherit file="../base.mako" />


<%block name="content">
<h2>Machines</h2>
<a href="/new/machine/">New Machine</a><br />
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>ID</th><th>Name</th><th>Description</th><th>Quantity</th><th>Action</th></tr>
            % for machine in machine_list:
                <tr><td>${machine.id}</td>
                <td><a href="/machine/${machine.id}/">${machine.name}</a></td>
                <td>${machine.description}</td>
                <td>${machine.quantity}</td>
                <td>
                    <a href="/edit/machine/${machine.id}/">Edit</a>
                    <a href="/delete/machine/${machine.id}/">Delete</a>
                </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>