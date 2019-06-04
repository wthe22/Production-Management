<%inherit file="../base.mako" />


<%block name="content">
<div style="width:100%;">
    <div class="horizontal-list" style="width:70%;">
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
    <div class="horizontal-list" style="width:30%; float:right;">
        <h3>Notifications</h3>
        <table class="striped" style="width:100%;">
            <tr><th>Time</th><th>Message</th><th>Action</th></tr>
            % for notification in notification_list:
                <tr>
                    <td>${notification.time}</td>
                    <td>${notification.title}</td>
                    <td><a href="${request.route_url('notification_delete', id=notification.id)}">Delete</a></td>
                </tr>
            % endfor
        </table>
    </div>
</div>
</%block>
