from client.answers.initiationAnswer import InitiationAnswer
from client.queries.initiationQuery import InitiationQuery


class apkeep:
    @staticmethod
    def init_model(network, snapshot):
        query = InitiationQuery("init_apkeep_model", network, snapshot)
        answer: InitiationAnswer = query.resolve()
        return answer.warpper()

    def detect_loops(self):
        pass
