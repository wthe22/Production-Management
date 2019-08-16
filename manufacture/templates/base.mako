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
        <div class="title">
            <img alt="Site Logo" src="/static/img/site_logo.png" />
            <h1><a href="/">Mining</a></h1>
        </div>
        <div class="navbar">
            <ul><%block name="navbar">
            % if view.is_authenticated:
                <li><a href="${request.route_url('home')}">Home</a></li>
                <li><a href="${request.route_url('item_list')}">Items & Reciepts</a></li>
                <li><a href="${request.route_url('stock_list')}">Inventory</a></li>
                <li><a href="${request.route_url('machine_list')}">Machines</a></li>
                <li><a href="${request.route_url('task_list')}">Task</a></li>
                <li><a href="${request.route_url('analyzer_input')}">Analyzer</a></li>
                <li>|</li>
                <li><a href="${request.route_url('user_logout')}">Logout</a></li>
            % else:
                <li><a href="${request.route_url('user_login')}">Login</a></li>
                <!-- style="float:right;" -->
            % endif
            </%block></ul>
        </div>
        <div class="content">
            <%block name="content">
            ${text}
            </%block>
        </div>
        <div class="footer">
            Copyright ${now.year} by wthe22. All Rights Reserved.<br />
        </div>
    </body>
</html>
