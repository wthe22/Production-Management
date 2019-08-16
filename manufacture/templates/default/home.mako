<%inherit file="../base.mako" />

<%!
import time
time_format = "%Y-%m-%d %H:%M:%S"
%>


<%block name="content">
<div style="width:100%;">
    <div class="horizontal-list" style="width:60%;">
        <h2>Production Management Website</h2>
        <br />
        <h3>本科毕业论文</h3>
        <br />
        <div>
            <h3>Technologies</h3>
            <div>
                <%
                powered_by_list = [
                    ["Python", "https://www.python.org/", "python-logo.png"],
                    ["Pyramid", "https://trypyramid.com/", "pyramid-small.png"],
                    ["Mako", "https://www.makotemplates.org/", "makoLogo.png"],
                    ["Peewee", "http://docs.peewee-orm.com/en/latest/", "peewee3-logo.png"],
                    ["SQLite", "https://www.sqlite.org/", "sqlite370_banner.gif"],
                ]
                %>
                % for name, website, img_name in powered_by_list:
                    <div class="horizontal-list"><a href="${website}">
                        <img src="/static/img/home/${img_name}" alt="{name}" style="height: 50px; margin: 10px;">
                    </a></div>
                % endfor
            </div>
        </div>
    </div>
    <div class="horizontal-list" style="width:40%; float:right;">
        <h3>Notifications</h3>
        <table class="striped" style="width:100%; height: 50vh;">
            <thead>
                <tr><th>Time</th><th>Message</th><th>Action</th></tr>
            </thead>
            <tbody>
            % for notification in notification_list:
                <tr>
                    <td>${time.strftime(time_format, time.localtime(notification.time))}</td>
                    <td>${notification.description}</td>
                    <td><a href="${request.route_url('notification_delete', id=notification.id)}">Delete</a></td>
                </tr>
            % endfor
            </tbody>
        </table>
    </div>
</div>
</%block>
