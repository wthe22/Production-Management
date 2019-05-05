<%inherit file="base.mako" />


<%block name="content">

<script type="text/javascript">
class EditForm {
    constructor(name, level) {
        this.fields = [
            {id: "reg_full_name", desc: "Full Name"},
            {id: "reg_occupation", desc: "Occupation"},
            {id: "reg_email", desc: "E-mail"},
            {id: "reg_phone_num", desc: "Phone Number"},
            {id: "reg_wechat", desc: "WeChat ID"},
        ];
    }
    
    // Adding a method to the constructor
    greet() {
        return `${this.name} says hello.`;
    }
    clear_all() {
        for (var i = 0; i < this.fields.length; i++) {
            $("#" + this.fields[i].id).val('');
        }
    }
    validate() {
    for (var i = 0; i < this.fields.length; i++) {
        if ($("#" + this.fields[i].id).val() == "") {
            $("#" + this.fields[i].id).focus();
            alert(this.fields[i].desc + " is empty!");
            return false;
        }
    }
    return true;
}
</script>


<h2>${heading}</h2>
<div style="width: 33%">
<section class="edit_form">
    <h2>Admin Login</h2>
    The page you requested requires login<br />
    <br />
    <form action="?" method="post" name="registration" onsubmit="return validate_form();">
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
