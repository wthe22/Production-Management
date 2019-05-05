<%!
import datetime
now = datetime.datetime.today()
is_authenticated = True
%>

<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="shortcut icon" href="/static/favicon.ico" />
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css">
        <script src="/static/bootstrap/js/bootstrap.js"></script>
        <link rel="stylesheet" href="/static/default/css/default.css">
        <link rel="stylesheet" href="/static/default/css/bootstrap-duration-picker.css">
        <script src="/static/default/js/jquery.min.js"></script>
        <script src="/static/default/js/template-form.js"></script>
        <title>Site</title>
    </head>
    <body>
        <div id="title">
            <img alt="Site Logo" src="/static/img/site_logo.png" />
            <h1><a href="/">Mining</a></h1>
        </div>
        <div id="navbar">
            <ul><%block name="navbar">
            % if is_authenticated:
                <a href="${request.route_url('home')}"><li>HOME</li></a>
                <a href="${request.route_url('list_items')}"><li>ITEMS & RECIPES</li></a>
                <a href="${request.route_url('list_stocks')}"><li>INVENTORY</li></a>
                <a href="${request.route_url('list_machines')}"><li>MACHINES</li></a>
                <a href="${request.route_url('list_tasks')}"><li>TASK</li></a>
                <a href="${request.route_url('list_notifications')}"><li>NOTIFICATIONS</li></a>
                <a href="/logout/"><li style="float:right;">Logout</li></a>
            % else:
                <a href="${request.route_url('home')}"><li>HOME</li></a>
                <a href="/login/"><li style="float:right;">Login</li></a>
            % endif
            </%block></ul>
        </div>
        <div id="content">
            <%block name="content">
            ${text}
            </%block>
        </div>
        <div id="footer">
            Copyright ${now.year} by wthe22. All Rights Reserved.<br />
        </div>
    </body>
</html>
