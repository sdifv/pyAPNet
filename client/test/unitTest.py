import json

from client.akHelper.solveStatus import SolveStatus

if __name__ == '__main__':
    # file_path = '/home/yuhao/下载/forwarding-change-validation/layer1_topology.txt'
    #
    # with open(file_path, mode='r') as f:
    #     packet = {
    #         'data': f.read()
    #     }
    #     jstr = json.dumps(packet)
    #
    #     print(json.loads(jstr).get("data"))
    line = '> you  are me'
    print(line.split(" ", 1)[-1])

