<%!
import datetime
now = datetime.datetime.today()
is_authenticated = True
%>

<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="/static/css/default.css">
        <link rel="shortcut icon" href="/static/favicon.ico" />
        <script src="/static/js/jquery.min.js"></script>
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
            <a href="/"><li>HOME</li></a>
            <a href="/items/"><li>ITEMS</li></a>
            <a href="/stocks/"><li>INVENTORY</li></a>
            <a href="/machines/"><li>MACHINES</li></a>
            <a href="/tasks/"><li>TASK</li></a>
            <a href="/notifications/"><li>NOTIFICATIONS</li></a>
            <a href="/database/"><li>DATABASE</li></a>
            <a href="/logout/"><li style="float:right;">Logout</li></a>
            % else:
            <a href="/"><li>HOME</li></a>
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
