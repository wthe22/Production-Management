<%inherit file="base.mako" />


<%block name="content">
<h2>Notifications</h2>
<br />
<div style="width:100%; height:100%;">
    <div class="horizontal-list">
        <table class="striped" style="width:100%;">
            <tr><th>Time</th><th>Message</th><th>By</th><th>Action</th></tr>
            % for notification in notification_list:
                <tr><td>${notification.time}</td>
                <td>${notification.text}</td>
                <td>???</td>
                <td><a href="/delete/notification/${notification.id}">Delete</a></td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
