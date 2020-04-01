import sys
import traceback

from client.akHelper.fibsDiff import FibsDiff
from client.akHelper.pathHelper import PathHelper
from client.answers.fibsDiffAnswer import FibsDiffAnswer
from client.answers.initiationAnswer import InitiationAnswer
from client.answers.reachabilityAnswer import ReachabilityAnswer
from client.queries.incrementQuery import IncrementalQuery
from client.queries.initiationQuery import InitiationQuery


class apkeep:

    def __init__(self, network, snapshot):
        self.network = network
        self.snapshot = snapshot
        self.init_apkeep_model()

    def init_apkeep_model(self):
        query = InitiationQuery('init_apkeep_model',self.network,self.snapshot)
        answer: InitiationAnswer = query.resolve()
        return answer.wrapper()

    def get_update_rules(self, new_snapshot):
        base_path = PathHelper.get_snapshot_path(self.network, self.snapshot)
        ref_path = PathHelper.get_snapshot_path(self.network, new_snapshot)
        try:
            if PathHelper.check_data_exist(base_path) & PathHelper.check_data_exist(ref_path):
                query = FibsDiff(base_path, ref_path)
                answer: FibsDiffAnswer = query.resolve()
                return answer.wrapper()
        except IOError:
            traceback.print_exc()
            sys.exit(-1)

    def detect_loops(self, update_rules):
        query = IncrementalQuery('detect_loops', update_rules)
        answer: ReachabilityAnswer = query.resolve()
        print(answer.wrapper())


