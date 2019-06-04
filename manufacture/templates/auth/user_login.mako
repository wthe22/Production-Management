<%inherit file="../base.mako" />


<%block name="content">

<h2>User Login</h2>

<form id="post_form" action="?" method="post">
    <div class="horizontal-list" id="login_form"></div><br />
    <p>${login_msg}</p>
    <button type="submit" name="submit" value="submit">Submit</button>
</form>

<script type="text/javascript">
login_form = new EditForm({
    ...{
        "varname": "login_form",
        "id": "login_form",
        "form": "post_form"
    },
    ...${str(login_form_schema) | n},
})
login_form.load();
</script>
</%block>
