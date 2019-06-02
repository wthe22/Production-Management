class Component {
    static html_code(attributes) {
        var html_code = "";
        
        var generic_attributes = `` + 
            ` name="${attributes.name}"` +
            ` id="${attributes.id}"`;
        if (attributes.type == "select") {
            html_code += `<select ${generic_attributes}>`;
            html_code += `<option value>--- Select ---</option>`;
            for (var j = 0; j < attributes.options.length; j++) {
                let [value, text] = attributes.options[j];
                html_code += `<option`;
                if (value == attributes.value)
                    html_code += ` selected`;
                html_code += ` value="${value}">${text}</option>`;
            }
            html_code += `</select>`;
        }
        if (attributes.type == 'textarea') {
            html_code += `<textarea` +
                ` rows="4" cols="50"` +
                ` ${generic_attributes}"` +
                ` >` +
                `${attributes.value}` +
                `</textarea>`;
        }
        if (attributes.type == 'text') {
            html_code += `<input` +
                ` type="text"` +
                ` value="${attributes.value}"` +
                ` autocomplete="off"` +
                ` ${generic_attributes}` +
                ` />`;
        }
        if (attributes.type == 'password') {
            html_code += `<input` +
                ` type="password"` +
                ` autocomplete="off"` +
                ` ${generic_attributes}` +
                ` />`;
        }
        if (attributes.type == 'number') {
            html_code += `<input` +
                ` type="number"` +
                ` value="${attributes.value}"` +
                ` autocomplete="off"` +
                ` ${generic_attributes}` +
                ` />`;
            // Include min/max
        }
        if (attributes.type == 'datetime') {
            html_code += `<input` +
                ` type="hidden"` +
                ` value="${attributes.value}"` +
                ` ${generic_attributes}` +
                ` />`;
            
            var date = new Date(attributes.value * 1000);
            var local_iso_date = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().substring(0,16);
            html_code += `<input` +
                ` type="datetime-local"` +
                ` value="${local_iso_date}"` +
                ` autocomplete="off"` +
                ` id="${attributes.id}_iso8601"` +
                ` />`;
        }
        return html_code;
    }
}


class EditForm {
    constructor({varname, form, id, name, components}) {
        this.varname = varname;
        this.form = form;
        this.id = id;
        this.name = name;
        this.components = components;
        console.log(this.components)
    }
    
    clear_all() {
        for (var i = 0; i < this.components.length; i++) {
            $(`#${this.id}__${this.components[i].name}`).val('');
        }
    }
    
    validate() {
        for (var i = 0; i < this.components.length; i++) {
            var field = $(`#${this.id}__${this.components[i].name}`);
            if (this.components[i].type == 'datetime')
                field = $(`#${this.id}__${this.components[i].name}_iso8601`)
            if (this.components[i].required) {
                var value = field.val()
                if (value == null || value == '') {
                    console.log("EMPTY!")
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
        for (var i = 0; i < this.components.length; i++) {
            var label_html = this.components[i].label;
            if (this.components[i].required)
                label_html += ` <span style="color:#F00;">*</span>`;
            
            var attributes = {...this.components[i]};
            attributes.id = `${this.id}__${this.components[i].name}`;
            attributes.name = `${this.name}__${this.components[i].name}`;
            var component_html = Component.html_code(attributes);
            
            form_html += `<tr><td>${label_html}</td><td>${component_html}</td></tr>`;
        }
        form_html = `<table>${form_html}</table><br />`
        $(`#${this.id}`).append(form_html);
        
        // ! Add event listener to onsubmit
        //$(`#${this.form}`).on('submit', this.validate);
    }
}


class ArrayForm {
    constructor({varname, form, id, name, components}) {
        this.varname = varname;
        this.form = form;
        this.id = id;
        this.name = name;
        this.components = components;
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
        $(`#${this.name}`).val(json_data);
        return true;
    }
    
    add_row(overrides=[]) {
        var index = this.rows_added;
        var row_html = "";
        for (var i = 0; i < this.components.length; i++) {
            var attributes = {...this.components[i], ...overrides[i]};
            attributes.id = `${this.id}__[${index}][${this.components[i].name}]`;
            attributes.name = `${this.name}__[${index}][${this.components[i].name}]`;
            var component_html = Component.html_code(attributes);
            row_html += `<td>${component_html}</td>`;
        }
        row_html = `<tr id="${this.id}__table_row${index}">` +
            `${row_html}` +
            `<td><button onclick="${this.varname}.remove_row(${index});" type="button">Delete</button></td>` +
            `</tr>`;
        
        $(`#${this.id}__table`).append(row_html);
        this.rows_added += 1;
    }
    
    remove_row(index) {
        $(`#${this.id}__table_row${index}`).remove();
    }
    
    load() {
        this.rows_added = 0;
        var table_header = ``;
        for (var i = 0; i < this.components.length; i++) {
            table_header += `<td>${this.components[i].description}</td>`;
        }
        table_header = `<tr>${table_header}</tr>`;
        var form_html = `<input type="hidden" value="" id="${this.name}" name="${this.name}">` +
            `<table class="striped" id="${this.id}__table">${table_header}</table>` +
            `<button onclick="${this.varname}.add_row();" type="button">Add</button>`;
        $(`#${this.id}`).append(form_html);
    }
}

// ! Name and ID name analysis required
