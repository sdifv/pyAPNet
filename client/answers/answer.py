class Answer:
    def __init__(self, query, data):
        self.query = query
        self.data = data

    def loops(self):
        loops_res = self.data.get('loops')
        for loop in loops_res:
            print(loop)

    def blackhole(self):
        pass

    def describe(self):
        loops_num = len(self.data.get('loops'))
        print('loops : {}'.format(loops_num))



