import os
import pandas as pd

from client.akHelper.fibHelper import decimalism2ip


class FibsDiffAnswer:
    def __init__(self, query, data):
        self.query = query
        self.path = data

    def wrapper(self, mode):
        if mode == 'detail':
            return self.detail_answer()
        elif mode == 'general':
            return self.general_answer()

    def detail(self):
        pass

    def general(self):
        if os.path.exists(self.path):
            change = []
            action = []
            node = []
            ip = []
            length = []
            interface = []
            priority = []
            for line in open(self.path):
                elements = line.split()
                change.append(elements[0])
                action.append(elements[1])
                node.append(elements[2])
                ip.append(decimalism2ip(elements[3]))
                length.append(elements[4])
                interface.append(elements[5])
                priority.append(elements[6])
            data = {"operator": change, "action": action, "node": node, "prefix": ip,
                    "mask_length": length, "interface": interface, "priority": priority}
            frame = pd.DataFrame(data, columns=["operator", "action", "node", "prefix",
                                                "mask_length", "interface", "priority"])
            return frame
        else:
            print("updates file is not existing!")
            return None
