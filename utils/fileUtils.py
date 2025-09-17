import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def write_to_json(data: object, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, cls=SetEncoder)