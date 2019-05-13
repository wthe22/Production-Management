import time


class PostForm:
    @staticmethod
    def defaults():
        return {
            'generic': {
                'name': None,
                'label': None,
                'required': False,
                'value': '',
                #'multiple': False,
            },
            'number': {
                'min': '',
                'max': '',
            },
            'datetime': {
                'value': int(time.time()),
                'min': '',
                'max': '',
            },
            'select': {
                'options': [],
            },
        }

    def __init__(self, name, components, action="submit"):
        self.name = name
        self.action = action
        self.components = []
        for i, parameters in enumerate(components):
            type = parameters['type']
            field = dict(self.defaults()['generic'])
            if type in self.defaults():
                field.update(self.defaults()[type])
            field.update(parameters)
            self.components.append(field)

    def schema(self):
        def escape_html(value):
            return str(value).replace('&', '&amp;').replace('"', '&quot;')
        components_schema = '\n'
        for field in self.components:
            #field['name'] = "{}__{}".format(self.name, field['name'])
            field_schema = ""
            for key, value in field.items():
                str_value = value
                
                if value is None:
                    str_value = "''"
                
                if isinstance(value, bool):
                    str_value = str(str_value).lower()
                
                if isinstance(value, list):
                    str_value = ''
                    for val, label in value:
                        str_value += "['{}', '{}'], ".format(escape_html(val), escape_html(label))
                    str_value = "[{}]".format(str_value[:-2])
                
                if isinstance(value, str):
                    str_value = "'" + escape_html(str_value) + "'"
                
                field_schema += "'{}': {}, ".format(key, str_value)
            components_schema += "{" + field_schema[:-2] + "}, \n"
        return "'{}', '{}', [{}]".format(self.name, self.action, components_schema)

    def extract_values(self, params):
        values = {}
        for field in self.components:
            key = field['name']
            value = params.get("{}__{}".format(self.name, key), None)
            if value == '' and field['type'] == 'number':
                value = None
            values[key] = value
        return values
