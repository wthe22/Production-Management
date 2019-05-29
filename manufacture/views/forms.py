import time
import json


class PostForm:
    @property
    def defaults(self):
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
            field = dict(self.defaults['generic'])
            if type in self.defaults:
                field.update(self.defaults[type])
            field.update(parameters)
            self.components.append(field)

    def schema(self):
        json_schema = [self.name, self.action, self.components]
        return json.dumps(json_schema, ensure_ascii=False)

    def extract_values(self, params):
        values = {}
        for field in self.components:
            key = field['name']
            value = params.get("{}__{}".format(self.name, key), None)
            if value == '' and field['type'] == 'number':
                value = None
            values[key] = value
        return values
