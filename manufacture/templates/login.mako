<%inherit file="base.mako" />


<%block name="content">

<style>
.rows {
    width:100%;
    height:auto;
    overflow:hidden;
    margin: 5px;
}
.label {
    width:150px;
    float:left;
}
.required {
    color:#F00;
}
.input-row {
    width:250px;
    background-color:#FFF;
    float:left;
    position:relative;
}
</style>

<div style="width: 33%">
<section class="edit_form">
    <h2>Admin Login</h2>
    <br />
    <form action="?" method="post" name="registration" onsubmit="return validateForm();">
        <div class="rows">
            <div class="label">Username</div>
            <div class="input-row"><input type="text" class="textbox" autocomplete="off" name="login_username" id="login_username" value=""></div>
        </div>
        <div class="rows">
            <div class="label">Password</div>
            <div class="input-row"><input type="password" class="textbox" autocomplete="off" name="login_password" id="login_password" value=""></div>
        </div>
        <input type="submit" value="Login" name="login"/>
    </form>
</section>
<br />

</div>
<script type="text/javascript">
    deform.load()
</script>

</%block>
