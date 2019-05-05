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
            if (this.fields[i].type == "select") {
                form_html += "<select name=\"" + this.fields[i].id + "\" id=\"" + this.fields[i].id + "\">"
                for (var j = 0; j < this.fields[i].value.length; j++) {
                    form_html += "<option value=\"" + this.fields[i].value[j][0] + "\">"
                    form_html += this.fields[i].value[j][1] + "</option>"
                }
                form_html += "</select>"
            } else {
                form_html += "<input type=\"" + this.fields[i].type + "\" class=\"textbox\" autocomplete=\"off\"";
                form_html += "name=\"" + this.fields[i].id + "\" id=\"" + this.fields[i].id + "\" value=\"" + this.fields[i].value + "\">";
            }
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
        {id: "machine", desc: "Machine", type: "select", required: true, value: ${str(form_values['machine']) | n}},
        {id: "recipe", desc: "Recipe", type: "select", required: true, value: ${str(form_values['recipe']) | n}},
        {id: "comment", desc: "Comment", type: "text", required: false, value: "${form_values['comment']}"},
        {id: "start_time", desc: "Start Time", type: "number", required: true, value: ${form_values['start_time']}},
        {id: "end_time", desc: "End Time", type: "number", required: false, value: ${form_values['end_time']}},
    ],
);
model_edit_form.load();
</script>
</%block>
