<%inherit file="../base.mako" />


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

<script type="text/javascript">
</script>

<h2>${heading}</h2>
<div class="horizontal-list" style="width: 40%" id="model_edit_form"></div>
<div class="horizontal-list" style="width: 30%">
</div>

<script type="text/javascript">
class EditForm {
    constructor(id, fields) {
        this.id = id;
        this.fields = fields;
    }
    
    clear_all() {
        for (var i = 0; i < this.fields.length; i++) {
            $("#" + this.fields[i].id).val('');
        }
    }
    
    validate() {
        for (var i = 0; i < this.fields.length; i++) {
            if (this.fields[i].required) {
                if ($("#" + this.fields[i].id).val() == "") {
                    $("#" + this.fields[i].id).focus();
                    alert(this.fields[i].desc + " is empty!");
                    return false;
                }
            }
        }
        return true;
    }
    
    load() {
        var form_html = "";
        form_html += "<form action=\"?\" method=\"post\" name=\"edit_data\" onsubmit=\"return " + this.id + ".validate();\">";
        form_html += "<table>";
        
        for (var i = 0; i < this.fields.length; i++) {
            form_html += "<tr>";
            form_html += "<td>";
            form_html += this.fields[i].desc;
            if (this.fields[i].required)
                form_html += " <span class=\"required\">*</span>";
            form_html += "</td>";
            form_html += "<td>"
            form_html += "<input type=\"" + this.fields[i].type + "\" class=\"textbox\" autocomplete=\"off\"";
            form_html += "name=\"" + this.fields[i].id + "\" id=\"" + this.fields[i].id + "\" value=\"" + this.fields[i].value + "\">";
            form_html += "</td>";
            form_html += "</tr>";
        }
        form_html += "</table>";
        form_html += "<br />";
        form_html += "<input type=\"submit\" value=\"submit\" name=\"submit\"/>";
        form_html += "</form>";
        $("#" + this.id).append(form_html);
    }
}
model_edit_form = new EditForm(
    "model_edit_form",
    [
        {id: "name", desc: "Name", type: "text", required: true, value: "${form_values['name']}"},
        {id: "description", desc: "Description", type: "text", required: false, value: "${form_values['description']}"},
        {id: "duration", desc: "Duration", type: "number", required: false, value: ${form_values['duration']}},
    ],
);
model_edit_form.load();
</script>
</%block>
