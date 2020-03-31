

class InitiationAnswer:
    def __init__(self, query, status):
        self.query = query
        self.data = status.value

    def warpper(self):
        return 'status of {}: {}'.format(self.query, self.data)
