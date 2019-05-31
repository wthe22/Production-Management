<%!
import datetime
now = datetime.datetime.today()
%>

<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="shortcut icon" href="/static/favicon.ico" />
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css">
        <script src="/static/bootstrap/js/bootstrap.js"></script>
        <link rel="stylesheet" href="/static/default/css/default.css">
        <script src="/static/default/js/jquery.min.js"></script>
        <script src="/static/default/js/post-form.js"></script>
        <!-- Static URL Link: '$ {request.static_url('tutorial:static/app.css')}' -->
        <title><%block name="title">Site</%block></title>
    </head>
    <body>
        <div id="title">
            <img alt="Site Logo" src="/static/img/site_logo.png" />
            <h1><a href="/">Mining</a></h1>
        </div>
        <div id="navbar">
            <ul><%block name="navbar">
            % if view.is_authenticated:
                <a href="${request.route_url('home')}"><li>HOME</li></a>
                <a href="${request.route_url('item_list')}"><li>ITEMS & RECIPES</li></a>
                <a href="${request.route_url('stock_list')}"><li>INVENTORY</li></a>
                <a href="${request.route_url('machine_list')}"><li>MACHINES</li></a>
                <a href="${request.route_url('task_list')}"><li>TASK</li></a>
                <a href="${request.route_url('analyzer_input')}"><li>ANALYZER</li></a>
                <a href="${request.route_url('user_logout')}"><li style="float:right;">Logout</li></a>
            % else:
                <a href="${request.route_url('default')}"><li>HOME</li></a>
                <a href="${request.route_url('user_login')}"><li style="float:right;">Login</li></a>
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
