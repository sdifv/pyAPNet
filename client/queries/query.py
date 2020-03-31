from client.akHelper.linkHelper import linkHelper
from client.akHelper.solveStatus import SolveStatus


class Query:
    def __init__(self, query_name):
        self.name = query_name
        self.answer = None
        self.status = SolveStatus.START
        self.socket = linkHelper.link2server()

    def set_answer(self, query_answer):
        self.answer = query_answer

    def set_status(self, status):
        if status not in SolveStatus:
            print('error: status is not defined')

        self.status = status
        if self.status == SolveStatus.END:
            self.socket.close()

    def release_source(self):
        self.socket.close()





