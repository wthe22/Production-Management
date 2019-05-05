
class EditForm {
    constructor(id, fields) {
        this.id = id;
        this.fields = fields;
    }
    
    clear_all() {
        for (var i = 0; i < this.fields.length; i++) {
            $(`#${this.fields[i].id}`).val('');
        }
    }
    
    validate() {
        for (var i = 0; i < this.fields.length; i++) {
            if (this.fields[i].required) {
                if ($(`#${this.fields[i].id}`).val() == "") {
                    $(`#${this.fields[i].id}`).focus();
                    alert(`${this.fields[i].desc} is empty!`);
                    return false;
                }
            }
        }
        return true;
    }
    
    load() {
        var form_html = "";
        form_html += `<form action="?" method="post" onsubmit="return ${this.id}.validate();">`;
        form_html += "<table>";
        
        for (var i = 0; i < this.fields.length; i++) {
            form_html += "<tr>";
            form_html += "<td>";
            form_html += this.fields[i].desc;
            if (this.fields[i].required)
                form_html += " <span class=\"required\">*</span>";
            form_html += "</td>";
            
            form_html += "<td>";
            if (this.fields[i].type == "select") {
                form_html += `<select name="${this.fields[i].id}" id="${this.fields[i].id}">`;
                for (var j = 0; j < this.fields[i].value.length; j++) {
                    form_html += `<option value="${this.fields[i].value[j][0]}">${this.fields[i].value[j][1]}</option>`;
                }
                form_html += `</select>`;
            } else {
                form_html += `<input type="${this.fields[i].type}" class="textbox" autocomplete="off"`;
                form_html += ` name="${this.fields[i].id}" id="${this.fields[i].id}" value="${this.fields[i].value}"/>`;
            }
            form_html += "</td>";
            form_html += "</tr>";
        }
        form_html += "</table>";
        form_html += "<br />";
        form_html += `<input type="submit" value="Submit" name="submit"/>`;
        form_html += "</form>";
        $(`#${this.id}`).append(form_html);
    }
}