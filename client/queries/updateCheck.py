import json
import os

from client.akHelper.jsonHelper import warp_input
from client.akHelper.pathHelper import PathHelper
from client.akHelper.solveStatus import SolveStatus
from client.answers.answer import Answer
from client.queries.query import Query


class UpdateCheck(Query):

    def __init__(self, query_name, network, snapshot):
        Query.__init__(self, query_name)
        container = PathHelper.get_snapshot_path(network, snapshot)
        self.update_rules = os.path.join(container, 'realConfig', 'forwardRules')

    def send_update_request(self):
        data = warp_input('cmd', 'update_check')
        self.socket.sendall(data.encode('utf-8'))

    def send_update_data(self):
        with open(self.update_rules, mode='r') as f:
            packet = {
                'head': '/parsed/batch_updates',
                'body': f.read()
            }
            data = warp_input('data', self.name, packet)
            self.socket.sendall(data.encode('utf-8'))

        data = warp_input('cmd', 'update_over')
        self.socket.sendall(data.encode('utf-8'))

    def resolve(self):
        self.send_update_request()
        resp_json = self.socket.recv(1024).decode('utf-8')
        resp = json.loads(resp_json)

        if resp.get('type') == 'aka' and resp.get('query') == 'update check':
            self.set_status(SolveStatus.POST_DATA)
            self.send_update_data()

            while True:
                resp_json = []
                while True:
                    recv = self.socket.recv(1024).decode('utf-8')
                    if "END" in recv:
                        resp_json.append(recv[:recv.find("END")])
                        break
                    else:
                        resp_json.append(recv)
                    if len(resp_json) > 1:
                        last_buf = resp_json[-2] + resp_json[-1]
                        if "END" in last_buf:
                            resp_json[-2] = last_buf[:last_buf.find("END")]
                            resp_json.pop()
                            break

                resp = json.loads(''.join(resp_json))
                if resp.get('type') == 'aka' and resp.get('query') == 'update check':
                    break
                else:
                    answer = Answer(resp.get('query'), resp.get('data'))
            self.set_status(SolveStatus.END)
            return answer
        else:
            raise RuntimeError('update check failed!')
