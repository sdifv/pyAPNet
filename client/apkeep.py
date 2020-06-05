import sys
import traceback

from client.akHelper.fibsDiff import FibsDiff
from client.akHelper.pathHelper import PathHelper
from client.answers.fibsDiffAnswer import FibsDiffAnswer
from client.answers.initiationAnswer import InitiationAnswer
from client.answers.reachabilityAnswer import ReachabilityAnswer
from client.queries.updateCheck import UpdateCheck
from client.queries.baseCheck import BaseCheck


class APKeep:

    def __init__(self, network, snapshot):
        self.network = network
        self.snapshot = snapshot

    def base_check(self):
        """

        :param network:
        :param snapshot:
        :return:
        """
        network = self.network
        snapshot = self.snapshot

        query_name = 'base check'
        try:
            query = BaseCheck(query_name, network, snapshot)
            # answer: loops{size,data},...
            answer = query.resolve()
            answer.describe()
            return answer
        except RuntimeError:
            traceback.print_exc()
            sys.exit(-1)

    def update_check(self, new_snapshot):
        query_name = 'update check'
        try:
            update_rules = self.get_update_rules(new_snapshot)
            query = UpdateCheck(query_name, update_rules)
            answer = query.resolve()
            answer.describe()
            return answer
        except RuntimeError:
            traceback.print_exc()
            sys.exit(-1)

    def get_update_rules(self, new_snapshot):
        base_path = PathHelper.get_snapshot_path(self.network, self.snapshot)
        ref_path = PathHelper.get_snapshot_path(self.network, new_snapshot)
        if PathHelper.check_data_exist(base_path) & PathHelper.check_data_exist(ref_path):
            query = FibsDiff(base_path, ref_path)
            answer = query.resolve()
            return answer

    # def detect_loops(self, update_rules):
    #     try:
    #         query = UpdateCheck('detect_loops', update_rules)
    #         answer: ReachabilityAnswer = query.resolve()
    #         return answer.wrapper()
    #     except RuntimeError:
    #         traceback.print_exc()
    #         sys.exit(-1)


