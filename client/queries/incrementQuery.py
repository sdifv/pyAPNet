from client.akHelper.jsonHelper import warp_input
from client.akHelper.solveStatus import SolveStatus
from client.answers.reachabilityAnswer import ReachabilityAnswer
from client.queries.query import Query


class IncrementalQuery(Query):

    def __init__(self, query_name, update_rules):
        Query.__init__(self, query_name)
        self.update_rules = update_rules

    def send_request(self, query_name):
        data = warp_input('cmd', query_name)
        print('send cmd: '+ query_name)
        self.socket.sendall(data.encode('utf-8'))

    def send_update_data(self, update_rules):
        with open(update_rules, mode='r') as f:
            packet = {
                'head': '/parsed/batch_updates',
                'data': f.read()
            }
            data = warp_input('data', packet)
            print('send data: '+packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        data = warp_input('cmd', 'update_over')
        print('send cmd: '+data)
        self.socket.sendall(data.encode('utf-8'))

    def resolve(self):
        self.send_request(self.name)
        resp4request = self.socket.recv(1024)
        if resp4request.decode('utf-8') == 'received cmd: '+self.name:
            self.set_status(SolveStatus.READY)

        loops_res = []
        if self.status == SolveStatus.READY:
            self.send_update_data(self.update_rules)

            resp4update = self.socket.recv(1024)

            loops_res.append(resp4update.decode('utf-8'))

            self.set_status(SolveStatus.END)
            self.set_status(SolveStatus.SUCCESS)

        else:
            self.set_status(SolveStatus.FAIL)

        if self.status == SolveStatus.SUCCESS:
            self.answer = "\n".join(loops_res)

        print(self.status)
        return ReachabilityAnswer(self.name, self.status, self.answer)
