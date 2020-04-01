import sys
import traceback

from client.akHelper.fibsDiff import FibsDiff
from client.akHelper.pathHelper import PathHelper
from client.answers.fibsDiffAnswer import FibsDiffAnswer

if __name__ == '__main__':
    base_path = PathHelper.get_snapshot_path('forwarding-change-validation', 'base')
    ref_path = PathHelper.get_snapshot_path('forwarding-change-validation', 'change')
    try:
        if PathHelper.check_data_exist(base_path) & PathHelper.check_data_exist(ref_path):
            query = FibsDiff(base_path, ref_path)
            answer: FibsDiffAnswer = query.resolve()
            print(answer.wrapper('general'))
    except IOError:
        traceback.print_exc()
        sys.exit(-1)
