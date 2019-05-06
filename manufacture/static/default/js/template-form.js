
class EditForm {
    constructor(id, name, action, fields) {
        this.id = id;
        this.name = name;
        this.action = action;
        this.fields = fields;
    }
    
    clear_all() {
        for (var i = 0; i < this.fields.length; i++) {
            $(`#${this.id}__${this.fields[i].name}`).val('');
        }
    }
    
    validate() {
        for (var i = 0; i < this.fields.length; i++) {
            if (this.fields[i].required) {
                var value = $(`#${this.id}__${this.fields[i].name}`).val()
                if (value == null || value == '') {
                    $(`#${this.id}__${this.fields[i].name}`).focus();
                    alert(`${this.fields[i].label} is empty!`);
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
            form_html += this.fields[i].label;
            if (this.fields[i].required)
                form_html += ` <span style="color:#F00;">*</span>`;
            form_html += "</td>";
            
            form_html += "<td>";
            if (this.fields[i].type == "select") {
                form_html += `<select name="${this.name}__${this.fields[i].name}" id="${this.id}__${this.fields[i].name}">`;
                form_html += `<option value>--- Select ---</option>`;
                for (var j = 0; j < this.fields[i].options.length; j++) {
                    let [value, text] = this.fields[i].options[j];
                    form_html += `<option`;
                    if (value == this.fields[i].value)
                        form_html += ` selected`;
                    form_html += ` value="${value}">${text}</option>`;
                }
                form_html += `</select>`;
            }
            if (this.fields[i].type == "textarea") {
                form_html += `<textarea rows="4" cols="50"`
                form_html += ` name="${this.name}__${this.fields[i].name}" id="${this.id}__${this.fields[i].name}" >`;
                form_html += `${this.fields[i].value}</textarea>`
            }
            if (this.fields[i].type == "text") {
                form_html += `<input type="text" value="${this.fields[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.fields[i].name}" id="${this.id}__${this.fields[i].name}"/>`;
            }
            if (this.fields[i].type == "number") {
                form_html += `<input type="number" value="${this.fields[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.fields[i].name}" id="${this.id}__${this.fields[i].name}"/>`;
            }
            form_html += "</td>";
            
            form_html += "</tr>";
        }
        form_html += "</table>";
        form_html += "<br />";
        form_html += `<button type="submit" name="${this.action}" value="submit">Submit</button>`;
        form_html += "</form>";
        $(`#${this.id}`).append(form_html);
    }
}