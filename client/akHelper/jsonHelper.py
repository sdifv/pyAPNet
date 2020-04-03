import json


def warp_input(input_type, query_name, data=None):
    packet = {
        'type': input_type,
        'query': query_name,
        'data': data
    }
    return json.dumps(packet)+'\n'


def unpack_output(jstr):
    print(jstr)
    res = json.loads(jstr)
    if res.get('type') == 'aka':
        print(res.get('data'))
    elif res.get('type') == 'ans':
        ans = json.loads(res.get('data'))
        if ans.get('head') == 'detect_loops':
            print(ans.get('body'))


