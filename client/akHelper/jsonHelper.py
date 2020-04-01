import json


def warp_input(input_type, data, parms = None):
    packet = {
        'type': input_type,
        'params': parms,
        'content': data
    }
    return json.dumps(packet)+'\n'

