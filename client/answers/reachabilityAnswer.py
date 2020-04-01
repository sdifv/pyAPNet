from client.akHelper.solveStatus import SolveStatus


class ReachabilityAnswer:
    def __init__(self, query, status, data):
        self.query = query
        self.status = status
        self.data = data

    def wrapper(self):

        if self.status == SolveStatus.SUCCESS:
            return 'status of {0} : {1} \n {2}'.format(self.query, self.status.value, self.data)
        elif self.status == SolveStatus.FAIL:
            return 'status of {0} : {1} \n'.format(self.query, self.status.value)
