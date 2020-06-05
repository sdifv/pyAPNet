import json

from client.akHelper.jsonHelper import warp_input, unpack_output
from client.akHelper.solveStatus import SolveStatus
from client.answers.answer import Answer
from client.answers.reachabilityAnswer import ReachabilityAnswer
from client.queries.query import Query


class UpdateCheck(Query):

    def __init__(self, query_name, update_rules):
        Query.__init__(self, query_name)
        self.update_rules = update_rules

    def send_update_request(self):
        data = warp_input('cmd', 'update_check')
        # print('send cmd: '+data)
        self.socket.sendall(data.encode('utf-8'))

    def send_update_data(self, update_rules):
        with open(update_rules, mode='r') as f:
            packet = {
                'head': '/parsed/batch_updates',
                'body': f.read()
            }
            data = warp_input('data', self.name, packet)
            # print('send data: '+packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        data = warp_input('cmd', 'update_over')
        # print('send cmd: '+data)
        self.socket.sendall(data.encode('utf-8'))

    def resolve(self):
        self.send_update_request()
        resp_json = self.socket.recv(1024).decode('utf-8')
        # print(resp_json)
        resp = json.loads(resp_json)

        if resp.get('type') == 'aka' and resp.get('query') == 'update check':
            self.set_status(SolveStatus.POST_DATA)
            self.send_update_data(self.update_rules.path)

            while True:
                json_str = self.socket.recv(4096).decode('utf-8')
                # print(json_str)
                resp = json.loads(json_str)
                # resp = json.loads(self.socket.recv(4096).decode('utf-8'))
                if resp.get('type') == 'aka' and resp.get('query') == 'update check':
                    break
                else:
                    answer = Answer(resp.get('query'), resp.get('data'))

            self.set_status(SolveStatus.END)
            return answer
        else:
            raise RuntimeError('update check failed!')


