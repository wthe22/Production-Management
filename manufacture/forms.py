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
        str_schema = ""
        for field in self.components:
            str_schema += "\n{"
            for key, value in field.items():
                str_value = value
                
                if value is None:
                    str_value = "''"
                elif isinstance(value, bool):
                    str_value = str(str_value).lower()
                elif isinstance(value, list):
                    str_value = str(str_value)
                else:
                    str_value = "\"" + str(str_value).replace('&', '&amp;').replace('"', '&quot;') + "\""
                str_schema += "'{}': {}, ".format(key, str_value)
            str_schema += "}, "
        return "'{}', '{}', [{}\n]".format(self.name, self.action, str_schema)
    
    def extract_values(self, params):
        values = {}
        print(params)
        for field in self.components:
            key = field['name']
            value = params.get("{}__{}".format(self.name, key), None)
            if value == '' and field['type'] == 'number':
                value = None
            values[key] = value
        return values
