class EditForm {
    constructor(id, schema) {
        this.id = id;
        [this.name, this.action, this.components] = schema
    }
    
    clear_all() {
        for (var i = 0; i < this.components.length; i++) {
            $(`#${this.id}__${this.components[i].name}`).val('');
        }
    }
    
    validate() {
        for (var i = 0; i < this.components.length; i++) {
            var field = $(`#${this.id}__${this.components[i].name}`)
            if (this.components[i].type == 'datetime')
                field = $(`#${this.id}__${this.components[i].name}_iso8601`)
            if (this.components[i].required) {
                var value = field.val()
                if (value == null || value == '') {
                    field.focus();
                    alert(`${this.components[i].label} is empty!`);
                    return false;
                }
            }
            if (this.components[i].type == 'datetime') {
                var date = new Date(field.val())
                $(`#${this.id}__${this.components[i].name}`).val(date.getTime()/1000)
            }
        }
        return true;
    }
    
    load() {
        var form_html = "";
        form_html += `<form action="?" method="post" onsubmit="return ${this.id}.validate();">`;
        form_html += "<table>";
        
        for (var i = 0; i < this.components.length; i++) {
            form_html += "<tr>";
            
            form_html += "<td>";
            form_html += this.components[i].label;
            if (this.components[i].required)
                form_html += ` <span style="color:#F00;">*</span>`;
            form_html += "</td>";
            
            form_html += "<td>";
            if (this.components[i].type == "select") {
                form_html += `<select name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}">`;
                form_html += `<option value>--- Select ---</option>`;
                for (var j = 0; j < this.components[i].options.length; j++) {
                    let [value, text] = this.components[i].options[j];
                    form_html += `<option`;
                    if (value == this.components[i].value)
                        form_html += ` selected`;
                    form_html += ` value="${value}">${text}</option>`;
                }
                form_html += `</select>`;
            }
            if (this.components[i].type == 'textarea') {
                form_html += `<textarea rows="4" cols="50"`
                form_html += ` name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}" >`;
                form_html += `${this.components[i].value}</textarea>`
            }
            if (this.components[i].type == 'text') {
                form_html += `<input type="text" value="${this.components[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}"/>`;
            }
            if (this.components[i].type == 'password') {
                form_html += `<input type="password" value="${this.components[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}"/>`;
            }
            if (this.components[i].type == 'number') {
                form_html += `<input type="number" value="${this.components[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}"/>`;
            }
            if (this.components[i].type == 'datetime') {
                var date = new Date(this.components[i].value * 1000);
                var local_iso_date = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().substring(0,16);
                form_html += `<input type="hidden" value="${this.components[i].value}" autocomplete="off"`;
                form_html += ` name="${this.name}__${this.components[i].name}" id="${this.id}__${this.components[i].name}"/>`;
                form_html += `<input type="datetime-local" value="${local_iso_date}" autocomplete="off"`;
                form_html += ` id="${this.id}__${this.components[i].name}_iso8601"/>`;
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


class ArrayForm {
    constructor(form, name) {
        this.form = form;
        this.name = name;
    }
    
    deduce_value(prefix) {
        var raw_data = $(`#${this.form}`).serializeArray();
        var explored_prefix = [];
        var values = {};
        for (var i = 0; i < raw_data.length; i++) {
            var field_name = `${raw_data[i].name}`;
            if (field_name.slice(0, prefix.length) != prefix)
                continue;
            var remaining = field_name.slice(prefix.length);
            var index_regex = /(?:\[([^\]]*)\])?(.*)/;
            var index = index_regex.exec(remaining);
            if (index[1] === undefined || index[1] === "") {
                index[1] = Object.keys(values).length
                values[`${index[1]}`] = `${raw_data[i].value}`;
            } else {
                var next_prefix = `${prefix}[${index[1]}]`;
                if (!(explored_prefix.indexOf(next_prefix) > -1)) {
                    values[`${index[1]}`] = this.deduce_value(next_prefix);
                    explored_prefix.push(next_prefix);
                }
            }
        }
        return values;
    }
    
    validate() {
        var json_data = JSON.stringify(this.deduce_value(`${this.name}__`));
        console.log(json_data);
        
        $(`#${this.name}`).val(json_data);
        return true;
    }
}