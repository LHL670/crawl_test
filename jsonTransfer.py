import json


def jsontransfer(items):
    data = json.dumps(items)
    jsonStr = json.loads(data)
    return jsonStr
