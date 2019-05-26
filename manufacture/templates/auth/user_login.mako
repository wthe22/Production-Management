<%inherit file="../base.mako" />


<%block name="content">

<h2>User Login</h2>
<div class="horizontal-list" style="width: 50%" id="login_form"></div>
<p>${login_msg}</p>

<script type="text/javascript">
login_form = new EditForm("login_form", ${str(login_form_schema) | n})
login_form.load();
</script>

</%block>
