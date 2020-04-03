import os
import sys
import logging
import datetime
import pandas as pd

from client.akHelper.fibHelper import format_fib_entry
from client.answers.fibsDiffAnswer import FibsDiffAnswer


class FibsDiff:

    def __init__(self, base_path, ref_path):
        self.base_path = base_path
        self.ref_path = ref_path
        self.res_path = os.path.join(base_path, 'APKeep', 'init')

    def resolve(self):
        base_fibs = os.path.join(self.base_path, 'fibs')
        ref_fibs = os.path.join(self.ref_path, 'fibs')
        nodes = os.listdir(base_fibs)
        with open(os.path.join(self.res_path, 'batch_updates'), mode='w') as f:
            for node in nodes:
                file1 = os.path.join(base_fibs, node)
                file2 = os.path.join(ref_fibs, node)
                shell = "diff " + file1 + " " + file2
                output = os.popen(shell)
                for line in output.readlines():
                    if line.find("<") != -1:
                        line = line.split(' ', 1)[-1]
                        f.write(format_fib_entry('-', line, node))
                    elif line.find(">") != -1:
                        line = line.split(' ', 1)[-1]
                        f.write(format_fib_entry('+', line, node))
                    else:
                        continue
        updates_path = os.path.join(self.res_path, 'batch_updates')
        return FibsDiffAnswer('get_update_rules', updates_path)



